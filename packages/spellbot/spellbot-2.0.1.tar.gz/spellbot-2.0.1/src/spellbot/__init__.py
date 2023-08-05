import asyncio
import inspect
import logging
from datetime import datetime, timedelta
from functools import wraps
from os import getenv
from pathlib import Path

import click
import discord
import hupper
import requests
from sqlalchemy import exc
from sqlalchemy.sql import text

from spellbot._version import __version__
from spellbot.assets import ASSET_FILES, s
from spellbot.data import AuthorizedChannel, Data, Game, Server, Tag, User, WaitTime

# Application Paths
RUNTIME_ROOT = Path(".")
SCRIPTS_DIR = RUNTIME_ROOT / "scripts"
DB_DIR = RUNTIME_ROOT / "db"
DEFAULT_DB_URL = f"sqlite:///{DB_DIR}/spellbot.db"
TMP_DIR = RUNTIME_ROOT / "tmp"
MIGRATIONS_DIR = SCRIPTS_DIR / "migrations"

# Application Settings
ADMIN_ROLE = "SpellBot Admin"
CREATE_ENDPOINT = "https://us-central1-magic-night-30324.cloudfunctions.net/createGame"
AVG_QUEUE_TIME_WINDOW_MIN = 30


def to_int(s):
    try:
        return int(s)
    except ValueError:
        return None


def is_admin(channel, user_or_member):
    """Checks to see if given user or member has the admin role on this server."""
    member = (
        user_or_member
        if hasattr(user_or_member, "roles")  # members have a roles property
        else channel.guild.get_member(user_or_member.id)  # but users don't
    )
    return any(role.name == ADMIN_ROLE for role in member.roles) if member else False


def ensure_application_directories_exist():
    """Idempotent function to make sure needed application directories are there."""
    TMP_DIR.mkdir(exist_ok=True)
    DB_DIR.mkdir(exist_ok=True)


def paginate(text):
    """Discord responses must be 2000 characters of less; paginate breaks them up."""
    breakpoints = ["\n", ".", ",", "-"]
    remaining = text
    while len(remaining) > 2000:
        breakpoint = 1999

        for char in breakpoints:
            index = remaining.rfind(char, 1800, 1999)
            if index != -1:
                breakpoint = index
                break

        message = remaining[0 : breakpoint + 1]
        yield message
        remaining = remaining[breakpoint + 1 :]
        last_line_end = message.rfind("\n")
        if last_line_end != -1 and len(message) > last_line_end + 1:
            last_line_start = last_line_end + 1
        else:
            last_line_start = 0
        if message[last_line_start] == ">":
            remaining = f"> {remaining}"

    yield remaining


def command(allow_dm=True):
    """Decorator for bot command methods."""

    def callable(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            return await func(*args, **kwargs)

        wrapped.is_command = True
        wrapped.allow_dm = allow_dm
        return wrapped

    return callable


class SpellBot(discord.Client):
    """Discord SpellTable Bot"""

    def __init__(
        self, token="", auth="", db_url=DEFAULT_DB_URL, log_level=logging.ERROR,
    ):
        logging.basicConfig(level=log_level)
        loop = asyncio.get_event_loop()
        super().__init__(loop=loop)
        self.token = token
        self.auth = auth

        # During the processing of a command there will be valid SQLAlchemy session
        # object available for use, commits and rollbacks are handled automatically.
        self.session = None

        # We have to make sure that DB_DIR exists before we try to create
        # the database as part of instantiating the Data object.
        ensure_application_directories_exist()
        self.data = Data(db_url)

        # build a list of commands supported by this bot by fetching @command methods
        members = inspect.getmembers(self, predicate=inspect.ismethod)
        self._commands = [
            member[0]
            for member in members
            if hasattr(member[1], "is_command") and member[1].is_command
        ]

        self._begin_background_tasks(loop)

    def _begin_background_tasks(self, loop):  # pragma: no cover
        """Start up any periodic background tasks."""
        self.cleanup_expired_games_task(loop)
        self.cleanup_expired_wait_times_task(loop)

    def cleanup_expired_games_task(self, loop):  # pragma: no cover
        """Starts a task that deletes old games."""
        THIRTY_SECONDS = 30

        async def task():
            while True:
                await self.cleanup_expired_games()
                await asyncio.sleep(THIRTY_SECONDS)

        loop.create_task(task())

    async def cleanup_expired_games(self):
        """Deletes games older than the given window of minutes."""
        session = self.data.Session()
        try:
            expired = Game.expired(session)
            for game in expired:
                for user in game.users:
                    discord_user = self.get_user(user.xid)
                    if discord_user:
                        await discord_user.send(s("expired", window=game.server.expire))
                session.delete(game)
            session.commit()
        except exc.SQLAlchemyError as e:
            logging.error("error: cleanup_expired_games:", e)
            session.rollback()
            raise
        finally:
            session.close()

    def cleanup_expired_wait_times_task(self, loop):  # pragma: no cover
        """Starts a task that deletes old wait times data."""
        FIVE_MINUTES = 300

        async def task():
            while True:
                await self.cleanup_expired_waits(AVG_QUEUE_TIME_WINDOW_MIN)
                await asyncio.sleep(FIVE_MINUTES)

        loop.create_task(task())

    async def cleanup_expired_waits(self, window):
        """Deletes wait time data older than the given window of minutes."""
        session = self.data.Session()
        try:
            cutoff = datetime.utcnow() - timedelta(minutes=window)
            session.query(WaitTime).filter(WaitTime.created_at < cutoff).delete()
            session.commit()
        except exc.SQLAlchemyError as e:
            logging.error("error: cleanup_expired_waits:", e)
            session.rollback()
            raise
        finally:
            session.close()

    def run(self):  # pragma: no cover
        super().run(self.token)

    def create_game(self):  # pragma: no cover
        headers = {"user-agent": f"spellbot/{__version__}", "key": self.auth}
        r = requests.post(CREATE_ENDPOINT, headers=headers)
        return r.json()["gameUrl"]

    def ensure_user_exists(self, user):
        """Ensures that the user row exists for the given discord user."""
        db_user = self.session.query(User).filter(User.xid == user.id).first()
        if not db_user:
            db_user = User(xid=user.id)
            self.session.add(db_user)
        return db_user

    def ensure_server_exists(self, guild_xid):
        """Ensures that the server row exists for the given discord guild id."""
        server = self.session.query(Server).filter(Server.guild_xid == guild_xid).first()
        if not server:
            server = Server(guild_xid=guild_xid)
            self.session.add(server)
        return server

    @property
    def commands(self):
        """Returns a list of commands supported by this bot."""
        return self._commands

    async def process(self, message, prefix):
        """Process a command message."""
        tokens = message.content.split(" ")
        request, params = tokens[0].lstrip(prefix).lower(), tokens[1:]
        params = list(filter(None, params))  # ignore any empty string parameters
        if not request:
            return
        matching = [command for command in self.commands if command.startswith(request)]
        if not matching:
            await message.channel.send(s("not_a_command", request=request), file=None)
            return
        if len(matching) > 1 and request not in matching:
            possible = ", ".join(f"{prefix}{m}" for m in matching)
            await message.channel.send(s("did_you_mean", possible=possible), file=None)
        else:
            command = request if request in matching else matching[0]
            method = getattr(self, command)
            if not method.allow_dm and str(message.channel.type) == "private":
                return await message.author.send(s("no_dm"))
            mentions = message.mentions if message.channel.type != "private" else []
            logging.debug(
                "%s%s (channel=%s, author=%s, mentions=%s, params=%s)",
                prefix,
                command,
                message.channel,
                message.author,
                mentions,
                params,
            )
            self.session = self.data.Session()
            try:
                await method(prefix, message.channel, message.author, mentions, params)
                self.session.commit()
            except exc.SQLAlchemyError as e:
                logging.error(f"error: {request}:", e)
                self.session.rollback()
                raise
            finally:
                self.session.close()

    ##############################
    # Discord Client Behavior
    ##############################

    async def on_message(self, message):
        """Behavior when the client gets a message from Discord."""
        # don't respond to any bots
        if message.author.bot:
            return

        private = str(message.channel.type) == "private"

        # only respond in text channels and to direct messages
        if not private and str(message.channel.type) != "text":
            return

        # don't respond to yourself
        if message.author.id == self.user.id:
            return

        # only respond to command-like messages
        if not private:
            rows = self.data.conn.execute(
                text("SELECT prefix FROM servers WHERE guild_xid = :g"),
                g=message.channel.guild.id,
            )
            prefixes = [row.prefix for row in rows]
            prefix = prefixes[0] if prefixes else "!"
        else:
            prefix = "!"
        if not message.content.startswith(prefix):
            return

        if not private:
            # check for admin authorized channels on this server
            rows = self.data.conn.execute(
                text("SELECT name FROM authorized_channels WHERE guild_xid = :g"),
                g=message.channel.guild.id,
            )
            authorized_channels = set(row["name"] for row in rows)
            if authorized_channels and message.channel.name not in authorized_channels:
                return

        await self.process(message, prefix)

    async def on_ready(self):
        """Behavior when the client has successfully connected to Discord."""
        logging.debug("logged in as %s", self.user)

    ##############################
    # Bot Command Functions
    ##############################

    # Any method of this class with a name that is decorated by @command is detected as a
    # bot command. These methods should have a signature like:
    #
    #     @command(allow_dm=True)
    #     def command_name(self, channel, author,mentions, params)
    #
    # - `allow_dm` indicates if the command is allowed to be used in direct messages.
    # - `channel` is the Discord channel where the command message was sent.
    # - `author` is the Discord author who sent the command.
    # - `params` are any space delimitered parameters also sent with the command.
    #
    # The docstring used for the command method will be automatically used as the help
    # message for the command. To document commands with parameters use a & to delimit
    # the help message from the parameter documentation. For example:
    #
    #     """This is the help message for your command. & <and> [these] [are] [params]"""
    #
    # Where [foo] indicates foo is optional and <bar> indicates bar is required.

    @command(allow_dm=True)
    async def help(self, prefix, channel, author, mentions, params):
        """
        Sends you this help message.
        """
        usage = ""
        for command in self.commands:
            method = getattr(self, command)
            doc = method.__doc__.split("&")
            use, params = doc[0], ", ".join([param.strip() for param in doc[1:]])
            use = inspect.cleandoc(use)
            use = use.replace("\n", "\n> ")

            title = f"{prefix}{command}"
            if params:
                title = f"{title} {params}"
            usage += f"\n`{title}`"
            usage += f"\n>  {use}"
            usage += "\n"
        usage += "---"
        usage += (
            " \nPlease report any bugs and suggestions at"
            " <https://github.com/lexicalunit/spellbot/issues>!"
        )
        usage += "\n"
        usage += (
            "\n💜 You can help keep SpellBot running by supporting me on Ko-fi! "
            "<https://ko-fi.com/Y8Y51VTHZ>"
        )
        for page in paginate(usage):
            await author.send(page)

    @command(allow_dm=True)
    async def about(self, prefix, channel, author, mentions, params):
        """
        Get information about SpellBot.
        """
        embed = discord.Embed(title="SpellBot")
        thumb = (
            "https://raw.githubusercontent.com/lexicalunit/spellbot/master/spellbot.png"
        )
        embed.set_thumbnail(url=thumb)
        version = f"[{__version__}](https://pypi.org/project/spellbot/{__version__}/)"
        embed.add_field(name="Version", value=version)
        embed.add_field(
            name="Package", value="[PyPI](https://pypi.org/project/spellbot/)"
        )
        author = "[@lexicalunit](https://github.com/lexicalunit)"
        embed.add_field(name="Author", value=author)
        embed.description = (
            "_A Discord bot for [SpellTable](https://www.spelltable.com/)._\n"
            "\n"
            f"Use the command `{prefix}help` for usage details. "
            "Having issues with SpellBot? "
            "Please [report bugs](https://github.com/lexicalunit/spellbot/issues)!\n"
            "\n"
            "💜 Help keep SpellBot running by "
            "[supporting me on Ko-fi!](https://ko-fi.com/Y8Y51VTHZ)"
        )
        embed.url = "https://github.com/lexicalunit/spellbot"
        embed.set_footer(text="MIT © amy@lexicalunit et al")
        embed.color = discord.Color(0x5A3EFD)
        await channel.send(embed=embed, file=None)

    @command(allow_dm=False)
    async def play(self, prefix, channel, author, mentions, params):
        """
        Enter a play queue for a game on SpellTable.

        You can get in a queue with a friend by mentioning them in the command with the @
        character. You can also change the number of players from the default of four by
        using, for example, `!play size:2` to create a two player game.

        Up to five tags can be given as well. For example, `!play no-combo proxy` has
        two tags: `no-combo` and `proxy`. Look on your server for what tags are being
        used by your community members. Tags can **not** be a number like `5`. Be careful
        when using tags because the matchmaker will only pair you up with other players
        who've used **EXACTLY** the same tags.

        You can also specify a power level like `!play power:7` for example and the
        matchmaker will attempt to find a game with similar power levels for you. Note
        that players who specify a power level will never get paired up with players who
        have not, and vice versa. You will also not be matched up _exactly_ by power level
        as there is a fudge factor involved.

        If your server's admins have set the scope for your server to "channel", then
        matchmaking will only happen between other players who run this command in the
        same channel as you did. The default scope for matchmaking is server-wide.
        & [@mention-1] [@mention-2] [...] [size:N] [power:N] [tag-1] [tag-2] [...]
        """
        params = [param.lower() for param in params]
        user = self.ensure_user_exists(author)
        if user.waiting:
            return await author.send(s("play_already"))

        size = 4
        power = None
        for param in params:
            if param.startswith("size:"):
                size = to_int(param.replace("size:", ""))
            elif param.startswith("power:"):
                power = to_int(param.replace("power:", ""))

        if not size or not (1 < size < 5):
            return await author.send(s("play_size_bad"))

        if power and not (1 <= power <= 10):
            return await author.send(s("play_power_bad"))

        if len(mentions) >= size:
            return await author.send(s("play_too_many_mentions"))

        mentioned_users = []
        for mentioned in mentions:
            mentioned_user = self.ensure_user_exists(mentioned)
            if mentioned_user.waiting:
                return await author.send(s("play_mention_already", user=mentioned))
            mentioned_users.append(mentioned_user)

        tags = []
        tag_names = [
            param
            for param in params
            if not param.startswith("size:")
            and not param.startswith("power:")
            and not param.startswith("<")
            and not param.startswith("@")
            and not param.isdigit()
            and not len(param) >= 50
        ]
        if not tag_names:
            tag_names = ["default"]
        if len(tag_names) > 5:
            return await author.send(s("play_too_many_tags"))
        for tag_name in tag_names:
            tag = self.session.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                self.session.add(tag)
            tags.append(tag)

        server = self.ensure_server_exists(channel.guild.id)
        user.enqueue(
            server=server,
            channel_xid=channel.id,
            include=mentioned_users,
            size=size,
            power=power,
            tags=tags,
        )
        self.session.commit()

        found_discord_users = []
        if len(user.game.users) == size:
            for game_user in user.game.users:
                discord_user = self.get_user(game_user.xid)
                if not discord_user:  # game_user has left the server since queueing
                    game_user.dequeue()
                else:
                    found_discord_users.append(discord_user)

        if len(found_discord_users) == size:  # all players matched, game is ready
            game_url = self.create_game()
            players_s = ", ".join(
                [f"<@!{discord_user.id}>" for discord_user in found_discord_users]
            )
            tags_s = ", ".join([tag.name for tag in user.game.tags])
            channel_s = f"<#{channel.id}>"
            power_s = str(user.game.power)
            response = s(
                "play_ready",
                url=game_url,
                players=players_s,
                tags=tags_s,
                channel=channel_s,
                power=power_s,
            )

            for game_user, discord_user in zip(user.game.users, found_discord_users):
                await discord_user.send(response)
                dequeue_at = datetime.utcnow()
                seconds = (dequeue_at - game_user.queued_at).total_seconds()
                WaitTime.log(
                    self.session,
                    guild_xid=server.guild_xid,
                    channel_xid=channel.id,
                    seconds=seconds,
                )
            self.session.delete(user.game)
        else:  # still waiting on more players, game is pending
            average = WaitTime.average(
                self.session,
                guild_xid=server.guild_xid,
                channel_xid=channel.id,
                scope=server.scope,
                window_min=AVG_QUEUE_TIME_WINDOW_MIN,
            )
            for player in user.game.users:
                discord_user = self.get_user(player.xid)
                if discord_user:
                    if average:
                        response = s("play_queue_with_average", average=f"{average:.2f}")
                        await discord_user.send(response)
                    else:
                        await discord_user.send(s("play_queue"))

    @command(allow_dm=True)
    async def leave(self, prefix, channel, author, mentions, params):
        """
        Leave your place in the queue.
        """
        user = self.ensure_user_exists(author)
        if not user.waiting:
            return await author.send(s("leave_already"))

        user.dequeue()
        await author.send(s("leave"))

    @command(allow_dm=False)
    async def status(self, prefix, channel, author, mentions, params):
        """
        Show some details about the queues on your server.
        """
        server = self.ensure_server_exists(channel.guild.id)
        average = WaitTime.average(
            self.session,
            guild_xid=server.guild_xid,
            channel_xid=channel.id,
            scope=server.scope,
            window_min=AVG_QUEUE_TIME_WINDOW_MIN,
        )
        if average:
            await channel.send(s("status", average=f"{average:.2f}"))
        else:
            await channel.send(s("status_unknown"))

    @command(allow_dm=False)
    async def spellbot(self, prefix, channel, author, mentions, params):
        """
        Configure SpellBot for your server.

        The following subcommands are supported:

        * `channel <list>`: Set SpellBot to only respond in the given list of channels.
        * `prefix <string>`: Set SpellBot prefix for commands in text channels.
        * `scope <server|channel>`: Set matchmaking scope to server-wide or channel-only.
        * `expire <number>`: Set the number of minutes before pending games expire.

        _You must have the "SpellBot Admin" role to use any of these commands._
        & <subcommand> [subcommand parameters]
        """
        if not is_admin(channel, author):
            return await author.send(s("not_admin"))
        if not params:
            return await author.send(s("spellbot_missing_subcommand"))
        self.ensure_server_exists(channel.guild.id)
        command = params[0]
        if command == "channels":
            await self.spellbot_channels(prefix, channel, author, mentions, params[1:])
        elif command == "prefix":
            await self.spellbot_prefix(prefix, channel, author, mentions, params[1:])
        elif command == "scope":
            await self.spellbot_scope(prefix, channel, author, mentions, params[1:])
        elif command == "expire":
            await self.spellbot_expire(prefix, channel, author, mentions, params[1:])
        else:
            await author.send(s("spellbot_unknown_subcommand", command=command))

    async def spellbot_channels(self, prefix, channel, author, mentions, params):
        if not params:
            return await author.send(s("spellbot_channels_none"))
        self.session.query(AuthorizedChannel).filter_by(
            guild_xid=channel.guild.id
        ).delete()
        for param in params:
            self.session.add(AuthorizedChannel(guild_xid=channel.guild.id, name=param))
        return await author.send(
            s("spellbot_channels", channels=", ".join([f"#{param}" for param in params]))
        )

    async def spellbot_prefix(self, prefix, channel, author, mentions, params):
        if not params:
            return await author.send(s("spellbot_prefix_none"))
        prefix_str = params[0][0:10]
        server = (
            self.session.query(Server)
            .filter(Server.guild_xid == channel.guild.id)
            .one_or_none()
        )
        if server:
            server.prefix = prefix_str
        else:
            self.session.add(Server(guild_xid=channel.guild.id, prefix=prefix_str))
        return await channel.send(s("spellbot_prefix", prefix=prefix_str))

    async def spellbot_scope(self, prefix, channel, author, mentions, params):
        if not params:
            return await author.send(s("spellbot_scope_none"))
        scope_str = params[0].lower()
        if scope_str not in ("server", "channel"):
            return await author.send(s("spellbot_scope_bad"))
        server = (
            self.session.query(Server)
            .filter(Server.guild_xid == channel.guild.id)
            .one_or_none()
        )
        if server:
            server.scope = scope_str
        else:
            self.session.add(Server(guild_xid=channel.guild.id, scope=scope_str))
        return await channel.send(s("spellbot_scope", scope=scope_str))

    async def spellbot_expire(self, prefix, channel, author, mentions, params):
        if not params:
            return await author.send(s("spellbot_expire_none"))
        expire = to_int(params[0])
        if not expire or not (10 < expire < 60):
            return await author.send(s("spellbot_expire_bad"))
        server = (
            self.session.query(Server)
            .filter(Server.guild_xid == channel.guild.id)
            .one_or_none()
        )
        if server:
            server.expire = expire
        else:
            self.session.add(Server(guild_xid=channel.guild.id, expire=expire))
        return await author.send(s("spellbot_expire", expire=expire))


def get_db_env(fallback):  # pragma: no cover
    """Returns the database env var from the environment or else the given gallback."""
    value = getenv("SPELLTABLE_DB_ENV", fallback)
    return value or fallback


def get_db_url(database_env, fallback):  # pragma: no cover
    """Returns the database url from the environment or else the given fallback."""
    value = getenv(database_env, fallback)
    return value or fallback


def get_log_level(fallback):  # pragma: no cover
    """Returns the log level from the environment or else the given gallback."""
    value = getenv("SPELLTABLE_LOG_LEVEL", fallback)
    return value or fallback


@click.command()
@click.option(
    "-l",
    "--log-level",
    type=click.Choice(["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]),
    default="ERROR",
    help="Can also be set by the environment variable SPELLTABLE_LOG_LEVEL.",
)
@click.option("-v", "--verbose", count=True, help="Sets log level to DEBUG.")
@click.option(
    "-d",
    "--database-url",
    default=DEFAULT_DB_URL,
    help=(
        "Database url connection string; "
        "you can also set this via the SPELLBOT_DB_URL environment variable."
    ),
)
@click.option(
    "--database-env",
    default="SPELLBOT_DB_URL",
    help=(
        "By default SpellBot look in the environment variable SPELLBOT_DB_URL for the "
        "database connection string. If you need it to look in a different variable "
        "you can set it with this option. For example Heroku uses DATABASE_URL."
        "Can also be set by the environment variable SPELLTABLE_DB_ENV."
    ),
)
@click.version_option(version=__version__)
@click.option(
    "--dev",
    default=False,
    is_flag=True,
    help="Development mode, automatically reload bot when source changes",
)
def main(
    log_level, verbose, database_url, database_env, dev,
):  # pragma: no cover
    database_env = get_db_env(database_env)
    database_url = get_db_url(database_env, database_url)
    log_level = get_log_level(log_level)

    # We have to make sure that application directories exist
    # before we try to create we can run any of the migrations.
    ensure_application_directories_exist()

    client = SpellBot(
        token=getenv("SPELLBOT_TOKEN", None),
        auth=getenv("SPELLTABLE_AUTH", None),
        db_url=database_url,
        log_level="DEBUG" if verbose else log_level,
    )

    if dev:
        reloader = hupper.start_reloader("spellbot.main")
        reloader.watch_files(ASSET_FILES)

    client.run()


if __name__ == "__main__":
    main()

from datetime import datetime, timedelta
from pathlib import Path

import alembic
import alembic.config
from humanize import naturaldelta
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    and_,
    create_engine,
    func,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker
from sqlalchemy.sql.expression import label

from spellbot.constants import AVG_QUEUE_TIME_WINDOW_MIN

PACKAGE_ROOT = Path(__file__).resolve().parent
ASSETS_DIR = PACKAGE_ROOT / "assets"
ALEMBIC_INI = ASSETS_DIR / "alembic.ini"
VERSIONS_DIR = PACKAGE_ROOT / "versions"


Base = declarative_base()


class WaitTime(Base):
    __tablename__ = "wait_times"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    guild_xid = Column(BigInteger, nullable=False)
    channel_xid = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    seconds = Column(Integer, nullable=False)

    @classmethod
    def log(cls, session, *, guild_xid, channel_xid, seconds):
        row = WaitTime(guild_xid=guild_xid, channel_xid=channel_xid, seconds=seconds)
        session.add(row)

    @classmethod
    def average(cls, session, *, guild_xid, channel_xid, scope, window_min):
        filters = [
            WaitTime.guild_xid == guild_xid,
            WaitTime.created_at > datetime.utcnow() - timedelta(minutes=window_min),
        ]
        if scope == "channel":
            filters.append(WaitTime.channel_xid == channel_xid)
        row = (
            session.query(label("average", func.sum(WaitTime.seconds) / func.count()))
            .filter(and_(*filters))
            .one_or_none()
        )
        return row.average if row else None


class Server(Base):
    __tablename__ = "servers"
    guild_xid = Column(BigInteger, primary_key=True, nullable=False)
    prefix = Column(String(10), nullable=False, default="!")
    scope = Column(String(10), nullable=False, default="server")
    expire = Column(Integer, nullable=False, server_default=text("30"))  # minutes
    games = relationship("Game", back_populates="server")
    authorized_channels = relationship("AuthorizedChannel", back_populates="server")


class AuthorizedChannel(Base):
    __tablename__ = "authorized_channels"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    guild_xid = Column(
        BigInteger, ForeignKey("servers.guild_xid", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(100), nullable=False)
    server = relationship("Server", back_populates="authorized_channels")


games_tags = Table(
    "games_tags",
    Base.metadata,
    Column("game_id", Integer, ForeignKey("games.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    xid = Column(BigInteger, nullable=False)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="SET NULL"), nullable=True)
    queued_at = Column(DateTime, nullable=True)
    game = relationship("Game", back_populates="users")

    @property
    def waiting(self):
        return self.queued_at is not None

    def enqueue(self, *, server, channel_xid, include, size, power, tags):
        session = Session.object_session(self)
        guild_xid = server.guild_xid
        required_tag_ids = set(tag.id for tag in tags)
        considerations = (
            session.query(games_tags.c.game_id, func.count(games_tags.c.game_id))
            .filter(games_tags.c.tag_id.in_([tag.id for tag in tags]))
            .group_by(games_tags.c.game_id)
            .having(func.count(games_tags.c.game_id) == len(tags))
            .all()
        )
        valid_game_ids = []
        for row in considerations:
            game = session.query(Game).get(row.game_id)
            if not game:
                continue
            if game.url is not None:
                continue
            if set(tag.id for tag in game.tags) != required_tag_ids:
                continue
            if len(game.users) >= size - len(include):
                continue
            if game.guild_xid != guild_xid:
                continue
            if game.size != size:
                continue
            if (
                server.scope == "channel"
                and game.channel_xid
                and game.channel_xid != channel_xid
            ):
                continue
            if power:
                if not game.power:
                    continue
                if not (power - 2 <= game.power <= power + 2):
                    continue
            valid_game_ids.append(row.game_id)
        existing_game = (
            session.query(Game)
            .filter(Game.id.in_(valid_game_ids))
            .order_by(Game.created_at)
            .first()
        )
        now = datetime.utcnow()
        expires_at = now + timedelta(minutes=server.expire)
        if existing_game:
            self.game = existing_game
            self.game.updated_at = now
            self.game.expires_at = expires_at
        else:
            self.game = Game(
                channel_xid=channel_xid if server.scope == "channel" else None,
                created_at=now,
                expires_at=expires_at,
                guild_xid=guild_xid,
                power=power,
                size=size,
                tags=tags,
                updated_at=now,
            )
            session.add(self.game)
        self.queued_at = now
        for user in include:
            user.game = self.game
            user.queued_at = now

    def dequeue(self):
        session = Session.object_session(self)
        if self.game and len(self.game.users) == 1:
            session.delete(self.game)
        self.game = None
        self.queued_at = None


class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    size = Column(Integer, nullable=False)
    guild_xid = Column(
        BigInteger, ForeignKey("servers.guild_xid", ondelete="CASCADE"), nullable=False
    )
    channel_xid = Column(BigInteger)
    power = Column(Integer)
    url = Column(String(255))
    users = relationship("User", back_populates="game")
    tags = relationship("Tag", secondary=games_tags, back_populates="games")
    server = relationship("Server", back_populates="games")

    @classmethod
    def expired(cls, session):
        return (
            session.query(Game)
            .filter(and_(datetime.utcnow() >= Game.expires_at, Game.url == None))
            .all()
        )

    def to_str(self):
        session = Session.object_session(self)
        rvalue = ""
        if self.url:
            rvalue += "**Your SpellTable game is ready!**\n"
            rvalue += f"{self.url}\n"
        else:
            rvalue += (
                "**You have been entered in a play queue "
                f"for a {self.size} player game.**"
            )
            average = WaitTime.average(
                session,
                guild_xid=self.server.guild_xid,
                channel_xid=self.channel_xid,
                scope=self.server.scope,
                window_min=AVG_QUEUE_TIME_WINDOW_MIN,
            )
            if average:
                delta = naturaldelta(timedelta(seconds=average))
                rvalue += f" _The average wait time is {delta}._\n"
            else:
                rvalue += "\n"
        players = ", ".join(sorted([f"<@{user.xid}>" for user in self.users]))
        rvalue += f"Players: {players}\n"
        if self.channel_xid:
            rvalue += f"Channel: <#{self.channel_xid}>\n"
        if not (len(self.tags) == 1 and self.tags[0].name == "default"):
            tag_names = ", ".join(sorted([tag.name for tag in self.tags]))
            rvalue += f"Tags: {tag_names}\n"
        if self.power:
            rvalue += f"Power Level: {self.power}\n"
        return rvalue.strip()


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    games = relationship("Game", secondary=games_tags, back_populates="tags")


def create_all(connection, db_url):
    config = alembic.config.Config(str(ALEMBIC_INI))
    config.set_main_option("script_location", str(VERSIONS_DIR))
    config.set_main_option("sqlalchemy.url", db_url)
    config.attributes["connection"] = connection
    alembic.command.upgrade(config, "head")


def reverse_all(connection, db_url):
    config = alembic.config.Config(str(ALEMBIC_INI))
    config.set_main_option("script_location", str(VERSIONS_DIR))
    config.set_main_option("sqlalchemy.url", db_url)
    config.attributes["connection"] = connection
    alembic.command.downgrade(config, "base")


class Data:
    """Persistent and in-memory store for user data."""

    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(db_url, echo=False)
        self.conn = self.engine.connect()
        create_all(self.conn, db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = Base.metadata

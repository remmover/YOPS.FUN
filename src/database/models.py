import enum
from datetime import date

from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy import Integer, SmallInteger, String, Table, Text, func
from sqlalchemy import Enum
# from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship


from src.database.connect import Base


image_m2m_tag = Table(
    "image_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("image_id", Integer, ForeignKey("images.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class Image(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    '''about is a description about image'''
    about: Mapped[str] = mapped_column(Text, nullable=True)
    tags = relationship("Tag", secondary=image_m2m_tag, backref="images")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship('User', backref="images", lazy='joined')


class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    '''name is case insensitive without space series (man spaces are changed
       with one)'''
    name: Mapped[str] = mapped_column(String(63), nullable=False, unique=True)


class Role(enum.Enum):
    user: str = "User"
    moder: str = "Moderator"
    admin: str = "Administrator"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    '''username must be case insensitive unique because comments
       must always be uniquely identified without an email address'''
    username: Mapped[str] = mapped_column(String(50))
    '''email must be case insensitive unique to avoid spoofing'''
    email: Mapped[str] = mapped_column(String(250), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Enum] = mapped_column("role", Enum(Role), default=Role.user)
    created_at: Mapped[date] = mapped_column("created_at", DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column("updated_at", DateTime, default=func.now(),
                                             onupdate=func.now())
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    '''about is users description about self'''
    about: Mapped[str] = mapped_column(Text, nullable=True)
    '''refresh_token must be deleted after logout'''
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    '''is_active=False if user is banned'''
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    '''emo_ fields is used for emotional colorimeter by using ChatGPT'''
    emo_joy: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    emo_anger: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    emo_sadness: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    emo_surprise: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    emo_disgust: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    emo_fear: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    created_at: Mapped[date] = mapped_column("created_at", DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column("updated_at", DateTime, default=func.now(),
                                             onupdate=func.now())
    image_id: Mapped[int] = mapped_column(Integer, ForeignKey("images.id"),
                                          nullable=True)
    image: Mapped["Image"] = relationship('Image', backref="comments", lazy='joined')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship('User', backref="comments", lazy='joined')


class Star(Base):
    __tablename__ = "stars"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    created_at: Mapped[date] = mapped_column("created_at", DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column("updated_at", DateTime, default=func.now(),
                                             onupdate=func.now())
    image_id: Mapped[int] = mapped_column(Integer, ForeignKey("images.id"),
                                          nullable=True)
    image: Mapped["Image"] = relationship('Image', backref="stars", lazy='joined')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship('User', backref="stars", lazy='joined')


class Logout(Base):
    __tablename__ = "logouts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    access_token: Mapped[str] = mapped_column(String(255), nullable=False)

user = User()

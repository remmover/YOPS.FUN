import enum
from datetime import date

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum

from src.database.connect import Base


class Role(enum.Enum):
    user: str = "User"
    moder: str = "Moderator"
    admin: str = "Administrator"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[date] = mapped_column("created_at", DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column(
        "updated_at", DateTime, default=func.now(), onupdate=func.now()
    )
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    role: Mapped[Enum] = mapped_column("role", Enum(Role), default=Role.user)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    comment = relationship("Comment", back_populates="user")


class Comment(Base):
    tablename = "comments"

    id = mapped_column(Integer, primary_key=True, index=True)
    text = mapped_column(String, index=True)
    created_at = mapped_column(DateTime, nullable=False)
    update_ad = mapped_column(DateTime, nullable=False)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="comment", lazy="joined")

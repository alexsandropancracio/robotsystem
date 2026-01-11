from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text

from backend.api.database.base import Base


class User(Base):
    __tablename__ = "users"

    # =========================
    # IDENTIDADE
    # =========================
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    full_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # =========================
    # STATUS
    # =========================
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text("true"),
        nullable=False,
    )

    is_email_verified: Mapped[bool] = mapped_column(
        Boolean,
        server_default="false",
        nullable=False,
    )

    # =========================
    # AUDITORIA
    # =========================
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # =========================
    # RELACIONAMENTOS
    # =========================
    refresh_tokens = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    licenses = relationship(
        "License",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    activation_tokens = relationship(
        "ActivationToken",
        back_populates="user",
        cascade="all, delete-orphan",  # útil para deletar tokens se o usuário for deletado
    )
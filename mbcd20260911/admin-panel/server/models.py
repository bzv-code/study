"""Модели SQLAlchemy админ-панели: товар (Product) и лог ошибок входа (LoginAttempt).

Поля товара соответствуют модели Bouquet из backend/app/models/bouquet.py,
поэтому при переезде на основную БД PostgreSQL достаточно подменить Base/engine.
"""
from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(100), default="")
    description: Mapped[str] = mapped_column(String(1000), default="")
    price: Mapped[int] = mapped_column(Integer, default=0)  # цена в рублях
    photo_url: Mapped[str] = mapped_column(String(500), default="")
    is_active: Mapped[int] = mapped_column(Integer, default=1)  # показывать в каталоге
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "description": self.description,
            "price": self.price,
            "photo_url": self.photo_url,
            "is_active": bool(self.is_active),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class LoginAttempt(Base):
    """Защита от перебора пароля: считаем неудачные попытки по IP."""
    __tablename__ = "login_attempts"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip: Mapped[str] = mapped_column(String(64), index=True)
    at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

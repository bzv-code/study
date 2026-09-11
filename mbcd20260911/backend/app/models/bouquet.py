"""Модель букета: название, категория, состав, размеры/цены, фото."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Bouquet(Base):
    __tablename__ = "bouquets"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000), default="")
    price: Mapped[int] = mapped_column()  # цена в копейках/центах
    photo_url: Mapped[str] = mapped_column(String(500), default="")

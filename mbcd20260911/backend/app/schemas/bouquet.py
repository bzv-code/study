"""Pydantic-схемы букета для ответов API."""
from pydantic import BaseModel


class BouquetOut(BaseModel):
    id: int
    title: str
    category: str
    description: str
    price: int
    photo_url: str

    class Config:
        from_attributes = True

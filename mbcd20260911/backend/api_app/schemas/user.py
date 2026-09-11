"""Pydantic-схемы пользователя: профиль, адреса."""
from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    max_user_id: int
    full_name: str
    phone: str
    bonus_balance: int

    class Config:
        from_attributes = True

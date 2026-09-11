"""Разбор и валидация WebAppData, приходящего из mini app при каждом запросе к API."""
from urllib.parse import parse_qsl

from app.core.security import verify_max_init_data


def parse_init_data(init_data: str, bot_token: str) -> dict:
    if not verify_max_init_data(init_data, bot_token):
        raise ValueError("Invalid MAX WebAppData signature")

    data = dict(parse_qsl(init_data, keep_blank_values=True))
    # data содержит как минимум: user (JSON-строка), chat, auth_date, query_id, hash
    return data

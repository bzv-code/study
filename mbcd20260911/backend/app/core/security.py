"""Проверка подлинности стартовых параметров MAX mini app (WebAppData).

Алгоритм (см. https://dev.max.ru/docs/webapps/validation):
1. Мини-приложение при запуске получает строку WebAppData в хеше URL
   (доступна на фронтенде как window.WebApp.initData).
2. Backend разбирает её на пары key=value, убирает поле hash, сортирует
   оставшиеся пары и склеивает через '\n' в строку launch_params.
3. Считает HMAC-SHA256(launch_params, key=secret_key), где secret_key
   выводится из токена бота, переводит в hex и сравнивает с полем hash.

Совпадение подписей означает, что данные пришли от MAX и не были подделаны.
"""
import hashlib
import hmac
from urllib.parse import parse_qsl


def verify_max_init_data(init_data: str, bot_token: str) -> bool:
    if not init_data or not bot_token:
        return False

    pairs = parse_qsl(init_data, keep_blank_values=True)
    data = dict(pairs)
    received_hash = data.pop("hash", None)
    if not received_hash:
        return False

    launch_params = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    computed_hash = hmac.new(secret_key, launch_params.encode(), hashlib.sha256).hexdigest()

    return hmac.compare_digest(computed_hash, received_hash)

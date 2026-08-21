from datetime import datetime

from zoneinfo import ZoneInfo


MSK = ZoneInfo("Europe/Moscow")


# =====================================
# Тихие часы: с 00:10 до 05:50 МСК
# уведомления НЕ проверяются
# =====================================

BLACKOUT_START = (0, 10)   # 00:10
BLACKOUT_END = (5, 50)     # 05:50



def now_msk():
    """
    Текущее время в московском часовом поясе
    """

    return datetime.now(MSK)



def is_alert_check_allowed():
    """
    True  — проверка уведомлений РАЗРЕШЕНА
    False — сейчас тихие часы (00:10–05:50 МСК)
    """

    now = now_msk()

    minutes = now.hour * 60 + now.minute

    start = BLACKOUT_START[0] * 60 + BLACKOUT_START[1]
    end = BLACKOUT_END[0] * 60 + BLACKOUT_END[1]

    return not (start <= minutes < end)
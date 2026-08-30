import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time

# Словарь для расчета шага пагинации в миллисекундах
TIMEFRAME_MS = {
    '1m': 60 * 1000,
    '3m': 3 * 60 * 1000,
    '5m': 5 * 60 * 1000,
    '15m': 15 * 60 * 1000,
    '30m': 30 * 60 * 1000,
    '1h': 60 * 60 * 1000,
    '2h': 2 * 60 * 60 * 1000,
    '4h': 4 * 60 * 60 * 1000,
    '6h': 6 * 60 * 60 * 1000,
    '12h': 12 * 60 * 60 * 1000,
    '1d': 24 * 60 * 60 * 1000,
    '1w': 7 * 24 * 60 * 60 * 1000
}


def get_bybit_data_range(symbol="BTC", start_date=None, end_date=None, market="spot", timeframe="1d"):
    """
    Получение данных за большой период с автоматической пагинацией.
    """
    if timeframe not in TIMEFRAME_MS:
        print(f"❌ Неверный таймфрейм: {timeframe}. Доступные: {', '.join(TIMEFRAME_MS.keys())}")
        return None

    exchange = ccxt.bybit({
        'enableRateLimit': True,
        'options': {
            'defaultType': market,
        }
    })

    symbol_formatted = f"{symbol}/USDT"

    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    if not end_date:
        end_date = datetime.now()

    current_since = int(start_date.timestamp() * 1000)
    end_timestamp = int(end_date.timestamp() * 1000)
    step_ms = TIMEFRAME_MS[timeframe]

    if current_since > end_timestamp:
        print(f"❌ Дата начала ({start_date}) позже даты окончания ({end_date})")
        return None

    print(
        f"📡 Загрузка {symbol_formatted} [{timeframe}] с {start_date.strftime('%Y-%m-%d')} по {end_date.strftime('%Y-%m-%d')}")

    all_ohlcv = []

    try:
        request_count = 0
        while current_since < end_timestamp:
            request_count += 1

            ohlcv = exchange.fetch_ohlcv(
                symbol=symbol_formatted,
                timeframe=timeframe,
                since=current_since,
                limit=1000
            )

            if not ohlcv:
                break

            all_ohlcv.extend(ohlcv)
            last_timestamp = ohlcv[-1][0]

            # Защита от бесконечного цикла
            if last_timestamp <= current_since:
                break

            # Сдвигаем время на 1 шаг таймфрейма вперед
            current_since = last_timestamp + step_ms

            if len(ohlcv) < 1000:
                break

            if request_count % 10 == 0:
                print(f"   ...загружено {len(all_ohlcv)} свечей (запрос #{request_count})")

            time.sleep(0.2)

        if not all_ohlcv:
            print(f"❌ Нет данных для {symbol} за указанный период")
            return None

        df = pd.DataFrame(
            all_ohlcv,
            columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
        )
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        # Фильтруем по датам и удаляем дубликаты
        df = df[(df.index >= start_date) & (df.index <= end_date)]
        df = df[~df.index.duplicated(keep='first')]
        df['coin'] = symbol

        print(f"✅ Загружено {len(df)} свечей за {request_count} запрос(ов)")
        if not df.empty:
            print(f"   Период: с {df.index.min()} по {df.index.max()}")

            # Предупреждение об отсутствии старых данных
            if df.index.min() > start_date + timedelta(days=30):
                print(
                    f"⚠️ Внимание: Запрошен период с {start_date.strftime('%Y-%m-%d')}, но данные начинаются с {df.index.min().strftime('%Y-%m-%d')}.")
                print(
                    f"   (Bybit не хранит минутные/часовые свечи бесконечно. Это максимальная доступная глубина истории).")

        return df

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None


def parse_coins_list(coins_list, start_date, end_date=None, market="spot", timeframe="1d", save_csv=True, delay=1.0):
    """
    Массовый парсинг списка монет за указанный период.
    """
    print("=" * 70)
    print(f"🚀 МАССОВЫЙ ПАРСИНГ {len(coins_list)} МОНЕТ")
    print(f"   Рынок: {market}")
    print(f"   Таймфрейм: {timeframe}")

    if isinstance(start_date, str):
        print(f"   Начало периода: {start_date}")
    else:
        print(f"   Начало периода: {start_date.strftime('%Y-%m-%d')}")

    if end_date:
        if isinstance(end_date, str):
            print(f"   Конец периода: {end_date}")
        else:
            print(f"   Конец периода: {end_date.strftime('%Y-%m-%d')}")
    else:
        print(f"   Конец периода: до сегодня")

    print(f"   Задержка между запросами: {delay}с (рекомендуется >= 1.0с для минутных свечей)")
    print("=" * 70)

    all_data = []
    successful_coins = []
    failed_coins = []

    start_time = time.time()

    for idx, coin in enumerate(coins_list, 1):
        print(f"\n[{idx}/{len(coins_list)}] 🔄 Обработка {coin}...")

        try:
            df = get_bybit_data_range(coin, start_date, end_date, market, timeframe)

            if df is not None and not df.empty:
                all_data.append(df)
                successful_coins.append(coin)
                print(f"✅ {coin}: успешно ({len(df)} свечей)")
            else:
                failed_coins.append(coin)
                print(f"⚠️ {coin}: нет данных")

        except Exception as e:
            failed_coins.append(coin)
            print(f"❌ {coin}: ошибка - {e}")

        if idx < len(coins_list):
            time.sleep(delay)

    elapsed_time = time.time() - start_time

    stats = {
        'total_coins': len(coins_list),
        'successful': len(successful_coins),
        'failed': len(failed_coins),
        'success_rate': (len(successful_coins) / len(coins_list)) * 100 if coins_list else 0,
        'elapsed_time': elapsed_time,
        'successful_coins': successful_coins,
        'failed_coins': failed_coins
    }

    print("\n" + "=" * 70)
    print("📊 СТАТИСТИКА ПАРСИНГА")
    print("=" * 70)
    print(f"   Всего монет: {stats['total_coins']}")
    print(f"   Успешно загружено: {stats['successful']}")
    print(f"   Не удалось загрузить: {stats['failed']}")
    print(f"   Процент успеха: {stats['success_rate']:.1f}%")
    print(f"   Время выполнения: {elapsed_time:.1f}с ({elapsed_time / 60:.1f} мин)")

    if failed_coins:
        print(f"\n⚠️ Не удалось загрузить ({len(failed_coins)}):")
        print(f"   {', '.join(failed_coins)}")

    if not all_data:
        print("\n❌ Нет данных для сохранения")
        return None, stats

    combined_df = pd.concat(all_data)
    combined_df = combined_df.sort_index()

    print(f"\n📊 ОБЪЕДИНЕННЫЕ ДАННЫЕ:")
    print(f"   Всего записей: {len(combined_df)}")
    print(f"   Уникальных монет: {combined_df['coin'].nunique()}")
    print(f"   Период: с {combined_df.index.min()} по {combined_df.index.max()}")

    if save_csv:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"all_coins_{market}_{timeframe}_{timestamp}.csv"
        combined_df.to_csv(filename)
        print(f"\n💾 Данные сохранены в {filename}")

        stats_filename = f"parsing_stats_{timeframe}_{timestamp}.txt"
        with open(stats_filename, 'w', encoding='utf-8') as f:
            f.write(f"Статистика парсинга - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n")
            f.write(f"Рынок: {market}\n")
            f.write(f"Таймфрейм: {timeframe}\n")
            f.write(f"Период: {start_date} - {end_date or 'наше время'}\n")
            f.write(f"Всего монет: {stats['total_coins']}\n")
            f.write(f"Успешно: {stats['successful']}\n")
            f.write(f"Не удалось: {stats['failed']}\n")
            f.write(f"Процент успеха: {stats['success_rate']:.1f}%\n")
            f.write(f"Время выполнения: {elapsed_time:.1f}с\n\n")
            f.write(f"Успешно загруженные монеты:\n")
            f.write(', '.join(successful_coins) + "\n\n")
            f.write(f"Не удалось загрузить:\n")
            f.write(', '.join(failed_coins) + "\n")
        print(f"💾 Статистика сохранена в {stats_filename}")

    print("=" * 70)
    return combined_df, stats


# ============================================
# ИСПОЛЬЗОВАНИЕ
# ============================================

if __name__ == "__main__":
    # Короткий список для тестов (замените на свой большой список при необходимости)
    COINS_LIST = ['BTC', 'ETH', 'SOL']

    # ========================================
    # ПРИМЕР 1: Часовые свечи (1h) за год
    # ========================================
    print("\n" + "=" * 70)
    print("📊 ПРИМЕР 1: BTC часовые свечи (1h) за 2024 год")
    print("=" * 70)

    df_btc_1h = get_bybit_data_range(
        symbol="BTC",
        start_date="2024-01-01",
        end_date="2024-12-31",
        market="spot",
        timeframe="1h"  # <-- Меняем таймфрейм здесь
    )

    if df_btc_1h is not None:
        filename = f"BTC_1h_2024_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df_btc_1h.to_csv(filename)
        print(f"💾 Сохранено в {filename}")

    # ========================================
    # ПРИМЕР 2: Минутные свечи (1m) за неделю
    # ========================================
    print("\n" + "=" * 70)
    print("📊 ПРИМЕР 2: BTC минутные свечи (1m) за последнюю неделю")
    print("=" * 70)

    # Вычисляем дату неделю назад
    one_week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')

    df_btc_1m = get_bybit_data_range(
        symbol="BTC",
        start_date=one_week_ago,
        end_date=today,
        market="spot",
        timeframe="1m"  # <-- Минутный таймфрейм
    )

    if df_btc_1m is not None:
        filename = f"BTC_1m_last_week_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df_btc_1m.to_csv(filename)
        print(f"💾 Сохранено в {filename}")

    # ========================================
    # ПРИМЕР 3: Массовый парсинг часовых свечей
    # ========================================
    print("\n" + "=" * 70)
    print("📊 ПРИМЕР 3: Массовый парсинг (1h) за последние 3 месяца")
    print("=" * 70)

    three_months_ago = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')

    combined_df, stats = parse_coins_list(
        coins_list=COINS_LIST,
        start_date=three_months_ago,
        end_date=today,
        market="spot",
        timeframe="1h",  # <-- Таймфрейм для массового парсинга
        save_csv=True,
        delay=1.0  # <-- Увеличена задержка для безопасности API
    )
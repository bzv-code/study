"""
Тестовый скрипт для проверки выгрузки зарубежных акций.
"""
from client.moex_client import MoexClient
from services.foreign_stock_service import ForeignStockService
from services.foreign_stock_candle_service import ForeignStockCandleService
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    logger.info("Starting foreign stock download test...")

    # Используем context manager для автоматического закрытия соединения
    with MoexClient(timeout=30) as client:
        stock_service = ForeignStockService(client)
        candle_service = ForeignStockCandleService(client, stock_service)

        # 1. Получаем список всех доступных зарубежных акций
        foreign_stocks = stock_service.get_all()
        logger.info(f"Total foreign stocks found: {len(foreign_stocks)}")

        # Выведем первые 10 для примера
        logger.info("First 10 foreign stocks:")
        for stock in foreign_stocks[:10]:
            logger.info(f" - {stock.secid}: {stock.shortname} (ISIN: {stock.isin})")

        # 2. Тестируем загрузку свечей для конкретной акции (например, Apple)
        test_secid = "AAPL-RM"
        logger.info(f"\nTesting candle download for {test_secid}...")

        try:
            candles = candle_service.get(
                secid=test_secid,
                date_from="2026-07-01",
                date_till="2026-08-26",
                interval=24  # Дневные свечи
            )
            logger.info(f"Successfully downloaded {len(candles)} candles for {test_secid}")
            if candles:
                latest = candles[-1]
                logger.info(f"Latest candle: Date={latest.begin.date()}, Close={latest.close}, Volume={latest.volume}")
        except Exception as e:
            logger.error(f"Failed to download candles for {test_secid}: {e}")


if __name__ == "__main__":
    main()
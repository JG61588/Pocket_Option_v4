"""Module for Pocket Option Candles websocket object."""
import logging
import time
from typing import List, Optional, Dict
from pocketoptionapi.ws.objects.base import Base
from pocketoptionapi.ws.objects.enhanced_candles import EnhancedCandles

logger = logging.getLogger(__name__)

class Candle:
    """Class for Pocket Option candle."""
    def __init__(self, candle_data: List):
        if len(candle_data) != 5:
            raise ValueError("Invalid candle data format")
        self.__candle_data = candle_data

    @property
    def candle_time(self) -> int:
        return self.__candle_data[0]

    @property
    def candle_open(self) -> float:
        return self.__candle_data[1]

    @property
    def candle_close(self) -> float:
        return self.__candle_data[2]

    @property
    def candle_high(self) -> float:
        return self.__candle_data[3]

    @property
    def candle_low(self) -> float:
        return self.__candle_data[4]

    @property
    def candle_type(self) -> str:
        if self.candle_open < self.candle_close:
            return "green"
        elif self.candle_open > self.candle_close:
            return "red"
        return "doji"

    def to_dict(self) -> dict:
        return {
            'time': self.candle_time,
            'open': self.candle_open,
            'close': self.candle_close,
            'high': self.candle_high,
            'low': self.candle_low
        }

class Candles(Base):
    """Class for Pocket Option Candles websocket object."""

    def __init__(self):
        super(Candles, self).__init__()
        self.__name = "candles"
        self.__candles_data: Optional[List] = None
        self.enhanced = EnhancedCandles()
        self.active_symbol: Optional[str] = None
        self.timeframe: Optional[int] = None

    @property
    def candles_data(self) -> Optional[List]:
        return self.__candles_data

    @candles_data.setter
    def candles_data(self, candles_data: List):
        if not isinstance(candles_data, list):
            logger.error("Invalid candles data format")
            return

        self.__candles_data = candles_data

        if candles_data and self.active_symbol and self.timeframe:
            try:
                # Обновляем все свечи в enhanced_candles
                for candle_data in candles_data:
                    candle = Candle(candle_data)
                    self.enhanced.update_realtime(
                        symbol=self.active_symbol,
                        timeframe=self.timeframe,
                        candle_data=candle.to_dict()
                    )
            except Exception as e:
                logger.error(f"Error updating candle data: {e}")

    def get_historical_candles(self, symbol: str, timeframe: int = 60,
                             count: int = 100, end_time: Optional[int] = None) -> List[Candle]:
        """
        Get historical candles with error handling and retries

        Args:
            symbol: Asset symbol (e.g. "EURUSD")
            timeframe: Timeframe in seconds (default: 60)
            count: Number of candles (default: 100)
            end_time: End timestamp (optional)

        Returns:
            List of Candle objects
        """
        try:
            # Сохраняем параметры
            self.active_symbol = symbol
            self.timeframe = timeframe

            # Запрашиваем данные через API
            if hasattr(self, 'api'):
                # Очищаем предыдущие данные
                self.__candles_data = None

                # Запрашиваем новые данные
                self.api.getcandles(symbol, timeframe, count, end_time or int(time.time()))

                # Ждем получения данных с таймаутом
                start_time = time.time()
                timeout = 5

                while self.__candles_data is None:
                    if time.time() - start_time > timeout:
                        logger.error(f"Timeout waiting for candles data for {symbol}")
                        return []
                    time.sleep(0.1)

                # Возвращаем обработанные свечи
                return self.get_candles(count)

            logger.error("API not initialized")
            return []

        except Exception as e:
            logger.error(f"Error getting historical candles: {e}")
            return []

    @property
    def first_candle(self) -> Optional[Candle]:
        if self.candles_data and len(self.candles_data) > 0:
            return Candle(self.candles_data[0])
        return None

    @property
    def second_candle(self) -> Optional[Candle]:
        if self.candles_data and len(self.candles_data) > 1:
            return Candle(self.candles_data[1])
        return None

    @property
    def current_candle(self) -> Optional[Candle]:
        if self.candles_data and len(self.candles_data) > 0:
            return Candle(self.candles_data[-1])
        return None

    def get_candles(self, count: int = 100) -> List[Candle]:
        """Get specified number of latest candles"""
        if not self.candles_data:
            return []
        return [Candle(data) for data in self.candles_data[-count:]]

"""Module for enhanced candles handling in Pocket Option API."""
import logging
import time
from datetime import datetime
from typing import List, Optional, Dict

logger = logging.getLogger(__name__)

class CandleData:
    """Enhanced candle data structure"""
    def __init__(self, time: int, open: float, close: float, high: float, low: float):
        self.time = time
        self.open = open
        self.close = close
        self.high = high
        self.low = low

class EnhancedCandles:
    """Enhanced candles handling class"""
    def __init__(self):
        self._candles_cache = {}
        self._last_request_time = {}  # Добавляем отслеживание времени запросов

    def update_realtime(self, symbol: str, timeframe: int, candle_data: dict):
        """Update realtime candle data"""
        try:
            cache_key = f"{symbol}_{timeframe}"
            if cache_key not in self._candles_cache:
                self._candles_cache[cache_key] = []

            # Проверяем, существует ли уже свеча с таким временем
            existing_candle = next(
                (candle for candle in self._candles_cache[cache_key]
                 if candle.time == candle_data['time']),
                None
            )

            if existing_candle:
                # Обновляем существующую свечу
                existing_candle.close = candle_data['close']
                existing_candle.high = max(existing_candle.high, candle_data['high'])
                existing_candle.low = min(existing_candle.low, candle_data['low'])
            else:
                # Добавляем новую свечу
                candle = CandleData(
                    time=candle_data['time'],
                    open=candle_data['open'],
                    close=candle_data['close'],
                    high=candle_data['high'],
                    low=candle_data['low']
                )
                self._candles_cache[cache_key].append(candle)

                # Сортируем свечи по времени
                self._candles_cache[cache_key].sort(key=lambda x: x.time)

        except Exception as e:
            logger.error(f"Error updating realtime candle: {e}")

    def get_candles(self, symbol: str, timeframe: int, count: int = 100) -> List[CandleData]:
        """Get cached candles for symbol and timeframe"""
        cache_key = f"{symbol}_{timeframe}"

        # Проверяем необходимость обновления данных
        current_time = int(time.time())
        if (cache_key not in self._last_request_time or
            current_time - self._last_request_time[cache_key] > timeframe):

            # Здесь должен быть вызов GetCandles для получения исторических данных
            end_time = current_time
            # api.get_candles(symbol, timeframe, count, end_time)

            self._last_request_time[cache_key] = current_time

        return self._candles_cache.get(cache_key, [])[-count:]

    def clear_cache(self, symbol: str = None, timeframe: int = None):
        """Clear candles cache"""
        if symbol and timeframe:
            cache_key = f"{symbol}_{timeframe}"
            self._candles_cache.pop(cache_key, None)
            self._last_request_time.pop(cache_key, None)
        else:
            self._candles_cache.clear()
            self._last_request_time.clear()
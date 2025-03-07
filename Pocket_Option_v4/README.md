# PocketOption API Library / Библиотека PocketOption API

## Features / Функции
- Auto-detect account type (Demo/Real) / Автоопределение типа аккаунта (Демо/Реальный)
- WebSocket connection management / Управление WebSocket подключением 
- Trade data handling and statistics / Обработка торговых данных и статистики
- Assets management and information / Управление и информация об активах

## Connection Examples / Примеры подключения
```python


>>>>>>>>>>>>>>>>>>>>>>>>>> Простое подключение / Simple Connection >>>>>>>>>>>>>>>>>>>>>>

from pocketoptionapi.api import PocketOptionAPI
# или / or
from pocketoptionapi.stable_api import PocketOption
import time

# SSID Example / Пример SSID
ssid = r'42["auth",{"session":"your_session","isDemo":1,"uid":your_uid,"platform":2}]'

# Connection / Подключение
api = PocketOptionAPI(ssid)  # автоматическое определение режима / auto-detect mode
# или / or
api = PocketOption(ssid)     # тоже автоматическое определение / also auto-detect mode

api.connect()
time.sleep(3)

# Check connection / Проверка подключения
print(f"Balance: {api.get_balance()}")  # Для PocketOption / For PocketOption
# или / or
print(f"Balance: {global_value.balance}")  # Для PocketOptionAPI / For PocketOptionAPI


>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

##Расширенное подключение с повторными попытками / Advanced Connection with Retries


def connect_with_retry(ssid, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            api = PocketOptionAPI(ssid)  # или PocketOption(ssid)
            api.connect()
            
            # Ждем подключения / Wait for connection
            timeout = 10
            start_time = time.time()
            while not global_value.websocket_is_connected:
                if time.time() - start_time > timeout:
                    raise Exception("Connection timeout")
                time.sleep(0.1)
                
            print(f"Successfully connected, Balance: {global_value.balance}")
            return api
            
        except Exception as e:
            print(f"Connection attempt {attempt + 1} failed: {e}")
            if attempt < max_attempts - 1:
                time.sleep(2)
    raise ConnectionError("Could not connect to API")

# Usage / Использование
api = connect_with_retry(ssid)

============================ Простое получение активов / Simple Assets =====================


# Get available assets / Получение доступных активов

from pocketoptionapi.stable_api import PocketOption
import time
ssid = r'your_ssid_here'  # Your session ID / Ваш идентификатор сессии
api = PocketOption(ssid=ssid)  #ручной режим определения режима SSID | manual mode for determining the SSID mode
api.connect()
time.sleep(3)

assets = api.get_assets()
for asset in assets:
    print(f"{asset.name} - {asset.symbol}")
    
>>>>>>>>>>>>>>>>>>>>>> Разделное получение активов / Separate receipt of assets >>>>>>>>>>>>>  

import time
from pocketoptionapi.api import PocketOptionAPI
ssid = r'your_ssid_here'  # Ваш идентификатор сессии / Your session ID
api = PocketOptionAPI(ssid) # Автомотическое определения режима SSID | Automatic detection of SSID mode
api.connect()
time.sleep(3)

api.print_assets_info()

>>>>>>>>>>>>>>>>>>> Полная информация по активам / Complete information on assets

# Get assets manager / Получение менеджера активов
manager = global_value.asset_manager

# Get assets by category / Получение активов по категориям
currencies = manager.get_assets_by_type("currency")     # Валютные пары / Currency pairs
stocks = manager.get_assets_by_type("stock")           # Акции / Stocks
crypto = manager.get_assets_by_type("cryptocurrency")  # Криптовалюты / Cryptocurrencies
commodities = manager.get_assets_by_type("commodity")  # Сырьевые товары / Commodities
indices = manager.get_assets_by_type("index")         # Индексы / Indices

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Print available currency pairs / Вывод доступных валютных пар
print("\nCurrency pairs / Валютные пары:")
for asset in currencies:
    if asset.is_available:
        print(f"{asset.name} ({asset.symbol})")
        
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Get specific asset details / Получение информации по конкретному активу 
eurusd = manager.get_asset_by_symbol("EURUSD_otc")
if eurusd:
    print(f"\nEUR/USD:")
    print(f"Available: {eurusd.is_available}")  # Доступен ли актив
    print(f"Type: {eurusd.type}")              # Тип актива

    
>>>>>>>>>>>>>>>>>>>>>>> работа с историей торгов / Simple Trade History >>>>>>>>>>>>>>>

# Get trade history / Получение истории сделок
trades = api.websocket_client.trade_handler.get_trade_history()
for trade_id, trade in trades.items():
    print(f"Trade {trade_id}:")           # Сделка
    print(f"Asset: {trade['asset']}")     # Актив
    print(f"Profit: {trade['profit']}")   # Прибыль
    
>>>>>>>>>>>>>>>>>>>>> Расширенная работа с историей торгов / Advanced Trade History >>>>>    

# Get trading statistics / Получение торговой статистики
stats = api.websocket_client.trade_handler.get_statistics()
print(f"Total trades: {stats['total_trades']}")  # Всего сделок
print(f"Win rate: {stats['win_rate']}%")        # Процент выигрышей
print(f"Total profit: {stats['total_profit']}")  # Общая прибыль

# Analysis of statistics / Анализ статистики
for category, data in stats.items():
    print(f"\n{category}:")
    print(f"Total trades: {data['total_trades']}")
    print(f"Profitable trades: {data['profitable_trades']}")
    print(f"Win rate: {data['win_rate']}%")
    print(f"Total profit: {data['total_profit']}")

>>>>>>>>>>>>>>>>>>>>>>>получение исторических данных / obtaining historical data>>>>>>>>>>>>>>>

##Простое получение свечей / Simple Candles

from pocketoptionapi.stable_api import PocketOption
import time

ssid = r'your_ssid_here'  # Your session ID / Ваш идентификатор сессии
api = PocketOption(ssid=ssid)
api.connect()
time.sleep(3)

# Get candles data / Получение данных свечей
candles = api.get_candles(
    active="EURUSD_otc",   # Asset symbol / Символ актива
    timeframe=300,         # Timeframe in seconds (300 = 5 minutes) / Таймфрейм в секундах (300 = 5 минут)
    count=20              # Number of candles / Количество свечей
)

# Print candles / Вывод свечей
for candle in candles:
    print(f"Time: {datetime.fromtimestamp(candle[0]).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Open: {candle[1]}")
    print(f"High: {candle[2]}")
    print(f"Low: {candle[3]}")
    print(f"Close: {candle[4]}")
    print("-" * 50)

>>>>>>>>>>>>>>>>>>>>> Расширенное получение свечей / Advanced Candles >>>>>>>>>>>>>

import time
from datetime import datetime
import logging
from pocketoptionapi.stable_api import PocketOption

# Setup logging / Настройка логирования
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_historical_data(symbol, timeframe, count):
    try:
        # Initialize API / Инициализация API
        ssid = r'your_ssid_here'
        api = PocketOption(ssid)
        
        # Connect / Подключение
        api.connect()
        time.sleep(3)

        print(f"\nRequesting data / Запрос данных:")
        print(f"Symbol: {symbol}")
        print(f"Timeframe: {timeframe} sec")
        print(f"Count: {count} candles")

        # Get candles / Получение свечей
        candles = api.get_candles(symbol, timeframe, count)

        if candles:
            print(f"\nReceived candles: {len(candles)}")
            print("\ntime, open, high, low, close")
            print("-" * 50)
            
            for candle in candles:
                time_str = datetime.fromtimestamp(candle[0]).strftime('%Y-%m-%d %H:%M:%S')
                print(f"{time_str}, {candle[1]:.5f}, {candle[2]:.5f}, {candle[3]:.5f}, {candle[4]:.5f}")

            return candles
        else:
            print("Failed to get candles data")
            return None

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return None
    
    finally:
        try:
            api.api.websocket_client = None
            logger.info("Connection closed")
        except Exception as e:
            logger.error(f"Error closing connection: {e}")

# Usage / Использование
candles = get_historical_data(
    symbol="EURUSD_otc",
    timeframe=300,  # 5 minutes / 5 минут
    count=20       # 20 candles / 20 свечей
)

>>>>>>>>>>>>>>>>>>>>>>>Открытие ордеров / Opening orders>>>>>>>>>>>>>>>>>>>>>>>

##Простое открытие ордера / Simple Order Opening

from pocketoptionapi.stable_api import PocketOption
import time

ssid = r'your_ssid_here'  # Your session ID / Ваш идентификатор сессии
api = PocketOption(ssid)
api.connect()
time.sleep(3)

# Buy order (CALL) / Покупка (CALL)
result, order_id = api.buy(
    amount=100,          # Amount / Сумма
    active="EURUSD_otc", # Asset / Актив
    action="call",       # Up direction / Направление вверх
    expirations=60       # Expiration in seconds / Время экспирации в секундах
)

# Check result / Проверка результата
if order_id:
    profit, status = api.check_win(order_id)
    print(f"CALL Order Profit: {profit}")
    print(f"Status: {status}")

# Sell order (PUT) / Продажа (PUT)
result, order_id = api.buy(
    amount=100,          
    active="EURUSD_otc", 
    action="put",        # Down direction / Направление вниз
    expirations=60       
)

if order_id:
    profit, status = api.check_win(order_id)
    print(f"PUT Order Profit: {profit}")
    print(f"Status: {status}")

>>>>>>>>>>>>>>>>>>>>> Расширенное открытие ордера (только на новой свече) / Advanced Order Opening (only on new candle) >>>>>>>>>>>>>

from pocketoptionapi.stable_api import PocketOption
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Buy order on new candle (CALL) / Покупка на новой свече (CALL)
result, order_id = api.buy_advanced(
    amount=100,          
    active="EURUSD_otc", 
    action="call",       # Up direction / Направление вверх
    expirations=60,      
    on_new_candle=True  # Wait for new candle / Ждать новую свечу
)

if order_id:
    profit, status = api.check_win(order_id)
    print(f"CALL Order Profit: {profit}")
    print(f"Status: {status}")

# Sell order on new candle (PUT) / Продажа на новой свече (PUT)
result, order_id = api.buy_advanced(
    amount=100,          
    active="EURUSD_otc", 
    action="put",        # Down direction / Направление вниз
    expirations=60,      
    on_new_candle=True  # Wait for new candle / Ждать новую свечу
)

if order_id:
    profit, status = api.check_win(order_id)
    print(f"PUT Order Profit: {profit}")
    print(f"Status: {status}")



>>>>>>>>>>>>>>>>>>>>>>>История сделок / Trade History>>>>>>>>>>>>>>>>>>>>>>>

##Простое получение истории / Simple Trade History

from pocketoptionapi.api import PocketOptionAPI
import time

ssid = r'your_ssid_here'  
api = PocketOptionAPI(ssid)
api.connect()
time.sleep(3)

# Get trade history / Получение истории сделок
trades = api.websocket_client.trade_handler.get_trade_history()

# Print trades / Вывод сделок
for trade_id, trade in trades.items():
    print(f"\nСделка ID: {trade_id}")
    print(f"Время открытия: {trade['openTime']}")
    print(f"Актив: {trade['asset']}")
    print(f"Сумма: {trade['amount']}")
    print(f"Прибыль: {trade['profit']}")
    print(f"Направление: {'CALL' if trade['direction'] == 0 else 'PUT'}")

>>>>>>>>>>>>>>>>>>>>> Расширенное получение истории / Advanced Trade History >>>>>>>>>>>>>

from pocketoptionapi.api import PocketOptionAPI
import time
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize API / Инициализация API
ssid = r'your_ssid_here'
api = PocketOptionAPI(ssid)
api.connect()
time.sleep(3)

# Set filter parameters / Установка параметров фильтрации
start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Get filtered history / Получение отфильтрованной истории
trades = api.websocket_client.trade_handler.get_filtered_history(
    asset="EURUSD_otc",           # Filter by asset / Фильтр по активу
    start_date=start_date,        # Start date / Начальная дата
    end_date=end_date,           # End date / Конечная дата
    is_demo=True,                # Demo account only / Только демо счет
    min_amount=100              # Minimum trade amount / Минимальная сумма сделки
)

# Get statistics / Получение статистики
stats = api.websocket_client.trade_handler.get_statistics_by_period(
    period_start=start_date,
    period_end=end_date
)

# Print statistics / Вывод статистики
print("\n=== Статистика торговли ===")
print(f"Всего сделок: {stats['total_trades']}")
print(f"Выигрышей: {stats['wins']}")
print(f"Проигрышей: {stats['losses']}")
print(f"Общая прибыль: {stats['total_profit']}")
print(f"Процент выигрышей: {stats['win_rate']:.2f}%")
print(f"Средняя прибыль: {stats['average_profit']:.2f}")

# Get detailed trade info / Получение детальной информации по сделке
if trades:
    trade_id = trades[0]['id']  # ID первой сделки
    details = api.websocket_client.trade_handler.get_trade_details(trade_id)
    
    if details:
        print("\n=== Детали сделки ===")
        print(f"ID: {details['id']}")
        print(f"Время открытия: {details['openTime']}")
        print(f"Время закрытия: {details['closeTime']}")
        print(f"Длительность: {details['duration_seconds']} сек")
        print(f"Актив: {details['asset']}")
        print(f"Изменение цены: {details['price_change']:.5f}")
        print(f"Процент изменения: {details['price_change_percent']:.2f}%")
        print(f"Направление: {details['direction_str']}")
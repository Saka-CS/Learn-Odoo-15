import configparser
import pathlib

from binance import client
from decimal import Decimal


config_path = str(pathlib.Path(__file__).parent.absolute()) + '/config.ini'
config = configparser.ConfigParser()
config.read(config_path)
api_key = config['Binance']['api_key']
secret_key = config['Binance']['secret_key']
btc_default_amount_to_buy = Decimal(config['Binance']['btc_default_amount_to_buy'])

# Create clients
bClient_Exc = client.Client(api_key, secret_key)
exchange_info = bClient_Exc.get_exchange_info()
exchange_info_dict = {}

# Get exchange info
for symbol_info in exchange_info['symbols']:
    exchange_symbol = symbol_info['symbol']
    quote_precision = symbol_info['quotePrecision']
    temp_step_size = symbol_info['filters'][2]['stepSize'].strip('0')
    lot_step_size = Decimal(temp_step_size).as_tuple().exponent * (-1)
    temp_price_tick_size = symbol_info['filters'][0]['tickSize'].strip('0')
    price_tick_size = Decimal(temp_price_tick_size).as_tuple().exponent * (-1)
    symbol_info_dict = {'quotePrecision': quote_precision, 'stepSize': lot_step_size, 'tickSize': price_tick_size}
    exchange_info_dict[exchange_symbol] = symbol_info_dict


def get_amount(symbol):
    balance = bClient_Exc.get_asset_balance(asset=symbol)
    return balance

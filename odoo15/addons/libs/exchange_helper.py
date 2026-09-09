from odoo.addons.binance_api import binance_api
from odoo.addons.gate_api import gate_api
from decimal import Decimal


def get_amount(exchange, symbol):
    if exchange == "Binance":
        balance = binance_api.get_amount(symbol)
        free = Decimal(balance['free'])
        locked = Decimal(balance['locked'])
        total = free + locked
    elif exchange == "Gate.io":
        total = gate_api.get_amount(symbol)
    elif exchange == "FTX":
        total = 0
    elif exchange == "pancake.swap":
        total = 0
    else:
        total = 0

    return total

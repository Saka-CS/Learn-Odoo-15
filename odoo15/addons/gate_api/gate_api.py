# !/usr/bin/env python
# coding: utf-8
import logging
import configparser
import pathlib
from decimal import Decimal as D

from . import ApiClient, Configuration, SpotApi


config_path = str(pathlib.Path(__file__).parent.absolute()) + '/config.ini'
config = configparser.ConfigParser()
config.read(config_path)
api_key = config['Gate.io']['api_key']
secret_key = config['Gate.io']['secret_key']

logger = logging.getLogger(__name__)

config = Configuration(key=api_key, secret=secret_key)
spot_api = SpotApi(ApiClient(config))


def get_amount(symbol):
    accounts = spot_api.list_spot_accounts(currency=symbol)
    assert len(accounts) == 1
    available = D(accounts[0].available)
    logger.info("Account available: %s %s", str(available), symbol)

    return available

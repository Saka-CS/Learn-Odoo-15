from odoo import models, fields


class CoinsCoin(models.Model):
    _name = 'coins.coin'
    _description = 'Coin'
    name = fields.Char('Name', required=True)
    symbol = fields.Char('Symbol', required=True)
    coin_portfolio_rows = fields.One2many('coins.portfolio_row', 'coin_id', string='Used Rows')

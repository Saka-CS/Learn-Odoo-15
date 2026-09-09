from odoo import models, fields


class CoinsExchange(models.Model):
    _name = 'coins.exchange'
    _description = 'Exchange'
    name = fields.Char('Name', required=True)
    exchange_apis = fields.One2many('coins.exchange_api', 'exchange_id', string='Usable APIs')
    exchange_portfolio_rows = fields.One2many('coins.portfolio_row', 'exchange_id', string='Used Rows')

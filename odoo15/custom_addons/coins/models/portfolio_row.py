from odoo import models, fields


class CoinsPortfolioRow(models.Model):
    _name = 'coins.portfolio_row'
    _description = 'Portfolio Row'
    portfolio_id = fields.Many2one('coins.portfolio', string='Portfolio')
    exchange_id = fields.Many2one('coins.exchange', string='Exchange', required=True)
    coin_id = fields.Many2one('coins.coin', string='Coin', required=True)
    amount = fields.Float('Amount')
    last_bought = fields.Float('Last Bought')

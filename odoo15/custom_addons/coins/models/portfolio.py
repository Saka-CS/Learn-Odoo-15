from odoo import models, fields
from odoo.addons.libs import exchange_helper


class CoinsPortfolio(models.Model):
    _name = 'coins.portfolio'
    _description = 'Portfolio'
    name = fields.Char('Name', required=True)
    portfolio_rows = fields.One2many('coins.portfolio_row', 'portfolio_id', string='Portfolio Rows')

    def action_get_amount(self):
        for portfolio_row in self.portfolio_rows:
            symbol = portfolio_row.coin_id.symbol
            exchange = portfolio_row.exchange_id.name
            total = exchange_helper.get_amount(exchange, symbol)
            portfolio_row.amount = total

        return True


"""     
        balance = binance_api.get_all(self, "ETH")
        balance = balance + 10
"""

from odoo import models, fields


class CoinsExchangeApi(models.Model):
    _name = 'coins.exchange_api'
    _description = 'Exchange API'
    name = fields.Char('Name', required=True)
    exchange_id = fields.Many2one('coins.exchange', string='Exchange')
    api_key = fields.Char('API Key', required=True)
    secret_key = fields.Char('Secret Key')

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    can_be_borrowed = fields.Boolean(default=False, string='Can be Borrowed')

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    able_to_be_borrowed = fields.Boolean(default=False, string='Able to be Borrowed')

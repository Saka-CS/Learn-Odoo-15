from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    borrow_request_ids = fields.One2many('borrow.request', 'product_id', string='Borrow Requests')
    can_be_borrowed = fields.Boolean(related='product_tmpl_id.can_be_borrowed', store=True, readonly=True)

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    can_be_borrowed = fields.Boolean(default=False, string='Can be Borrowed')
    borrow_request_ids = fields.One2many('borrow.request', 'product_tmpl_id', string='Borrow Requests')

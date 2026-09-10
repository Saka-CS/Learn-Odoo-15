from odoo import fields, models


class BorrowRequest(models.Model):
    _name = 'inventory.borrow.request'
    _description = 'A way for employees to borrow items if they are allowed to be borrowed'

    employee_id = fields.Many2one('hr.employee')
    product_id = fields.Many2many(
        'product.product', string='Product', domain="[('can_be_borrowed', '=', True)]"
    )

    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    state = fields.Selection(
        string='State',
        default='borrowed',
        selection=[
            ('borrowed', 'Borrowed'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled'),
        ],
        required=True,
    )

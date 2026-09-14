from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class BorrowRequest(models.Model):
    _name = 'borrow.request'
    _description = 'A way for employees to borrow items if they are allowed to be borrowed'

    def _default_employee(self):
        return self.env.user.employee_id.id

    employee_id = fields.Many2one('hr.employee', default=_default_employee, required=True, readonly=True)
    product_id = fields.Many2one(
        'product.product', string='Product', required=True, domain="[('can_be_borrowed', '=', True)]"
    )

    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product Template',
        related='product_id.product_tmpl_id',
        readonly=True,
        store=True,
    )

    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    state = fields.Selection(
        string='State',
        default='pending',
        selection=[
            ('pending', 'Pending'),
            ('borrowed', 'Borrowed'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled'),
        ],
        required=True,
        readonly=True,
    )

    @api.constrains('product_id')
    def _check_product_can_be_borrowed(self):
        for record in self:
            if record.product_id and not record.product_id.product_tmpl_id.can_be_borrowed:
                raise ValidationError(
                    _("Product '%s' cannot be borrowed. Enable 'Can be Borrowed' on the product template first.")
                    % record.product_id.display_name
                )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id and not self.product_id.product_tmpl_id.can_be_borrowed:
            return {'warning': {'title': _('Not borrowable'), 'message': _('This product cannot be borrowed.')}}

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class BorrowRequest(models.Model):
    _name = 'borrow.request'
    _description = 'A way for employees to borrow items if they are allowed to be borrowed'

    def _default_employee(self):
        return self.env.user.employee_id.id

    name = fields.Char(
        string='Reference', default=lambda self: _('New'), readonly=True, required=True, copy=False, index=True
    )
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
        # readonly=True,
        copy=False,
        tracking=True,
    )

    borrow_date = fields.Datetime(string='Borrow Date', default=lambda self: fields.Datetime.now())
    # expected_return_date = fields.Datetime(string='Expected Return Date')
    # return_date = fields.Datetime(string='The date the item was returned', readonly=True)

    picking_id = fields.Many2one('stock.picking', string='Delivery Transfer', readonly=True)
    return_picking_id = fields.Many2one('stock.picking', string='Return Transfer', readonly=True)

    _TRANSITIONS = {
        'pending': {'borrowed', 'canceled'},
        'borrowed': {'completed', 'canceled'},
        'completed': set(),
        'canceled': set(),
    }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('state', 'pending') != 'pending':
                raise UserError('You can not create a borrow request that does not start with pending state')

            vals.setdefault('borrow_date', fields.Datetime.now())

            if vals.get('name', _('New')) == _('New'):
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['borrow_date']))
                vals['name'] = self.env['ir.sequence'].next_by_code('borrow.request', sequence_date=seq_date)

        records = super().create(vals_list)

        # for record in records:
        #     record.picking_id = record._create_picking()
        return records

    def write(self, vals):
        if 'state' in vals:
            new_state = vals['state']
            for record in self:
                if new_state == record.state:
                    continue

                allowed_state_changes = self._TRANSITIONS.get(record.state) or set()
                if new_state not in allowed_state_changes:
                    raise UserError(_('Can not move from %s to %s') % (record.state, vals['state']))

            res = super().write(vals)
            if 'state' in vals:
                for record in self:
                    if record.state == 'borrowed' and not record.picking_id:
                        record.picking_id = record._create_picking(is_return=False)
                    elif record.state == 'completed' and not record.return_picking_id:
                        record.return_picking_id = record._create_picking(is_return=True)
            return res

        #         if new_state == 'borrowed':
        #             self._create_picking()
        #         elif new_state in {'borrowed', 'completed'}:
        #             self._create_picking(True)
        #
        # return super().write(vals)

    def _create_picking(self, is_return=False):
        for record in self:
            StockPicking = record.env['stock.picking']

            stock_location = record.env.ref('stock.stock_location_stock')
            employee_location = record.env.ref('inventory_borrow.location_employee_borrowed')
            picking_type = (
                record.env.ref('stock.picking_type_out') if not is_return else record.env.ref('stock.picking_type_in')
            )

            src_location = employee_location if is_return else stock_location
            dest_location = stock_location if is_return else employee_location

            picking_vals = {
                'picking_type_id': picking_type.id,
                'location_id': src_location.id,
                'location_dest_id': dest_location.id,
                'origin': record.name,
            }
            picking = StockPicking.create(picking_vals)

            move_vals = {
                'name': record.product_id.name,
                'product_id': record.product_id.id,
                'product_uom_qty': record.quantity,
                'product_uom': record.product_id.uom_id.id,
                'picking_id': picking.id,
                'location_id': src_location.id,
                'location_dest_id': dest_location.id,
            }
            self.env['stock.move'].create(move_vals)

            picking.action_confirm()
            picking.button_validate()

            return picking

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
            return {
                'warning': {'title': _('Not able to be borrowed'), 'message': _('This product cannot be borrowed.')}
            }

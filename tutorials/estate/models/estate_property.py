from dateutil.relativedelta import relativedelta
from odoo import api, exceptions, fields, models
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Contain the information of a real estate property'

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be a positive number'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be a positive number'),
    ]

    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('North', 'North'),
            ('South', 'South'),
            ('East', 'East'),
            ('West', 'West'),
        ]
    )

    state = fields.Selection(
        default='New',
        selection=[
            ('New', 'New'),
            ('Offer Received', 'Offer Received'),
            ('Offer Accepted', 'Offer Accepted'),
            ('Sold', 'Sold'),
            ('Canceled', 'Canceled'),
        ],
        required=True,
        copy=False,
    )
    active = fields.Boolean(default=True)

    estate_property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    seller_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offer')

    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price', store=True)

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'
            return
        self.garden_area = 0
        self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state in {'New', 'Offer Received', 'Offer Accepted', 'Sold'}:
                record.state = 'Sold'
            else:
                raise exceptions.UserError('Property can not be changed to sold')
        return True

    def action_canceled(self):
        for record in self:
            if record.state in {'New', 'Offer Received', 'Offer Accepted', 'Canceled'}:
                record.state = 'Canceled'
            else:
                raise exceptions.UserError('Property can not be changed to canceled')
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_percentage(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            if float_compare(record.selling_price, (record.expected_price * 0.90), precision_digits=2) < 0:
                raise exceptions.ValidationError('The selling price must be at least 90% more than the expected price')

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancled(self):
        for record in self:
            if record.state not in {'New', 'Canceled'}:
                raise exceptions.ValidationError(
                    'Error: Can not delete an estate property if it is not new or canceled'
                )

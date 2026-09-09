from datetime import timedelta

from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'An offer made by a user to buy and estate'

    _sql_constraints = [('check_offer_price', 'CHECK(price > 0)', 'The offer price must be a positive number')]
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')], copy=False)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(
        string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date', store=True
    )

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one(
        'estate.property.type', related='property_id.estate_property_type_id', store=True
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)
                continue
            record.date_deadline = record.create_date + timedelta(days=record.validity)

    @api.model
    def create(self, vals):
        property_id = self.env['estate.property'].browse(vals['property_id'])
        if property_id.state in {'Sold', 'Canceled'}:
            raise exceptions.UserError("You can't create a new offer for a property that is sold or canceled")

        if property_id.best_price >= vals['price']:
            raise exceptions.UserError('Offer price can not be lower than the offer with the highest price')

        if property_id.state == 'New':
            property_id.state = 'Offer Received'
        return super().create(vals)

    def _inverse_date(self):
        for record in self:
            if not record.date_deadline:
                record.validity = 0
                continue
            if not record.create_date:
                record.validity = (record.date_deadline - fields.Date.today()).days
                continue
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for record in self:
            if record.status == 'Accepted':
                raise exceptions.UserError('The offer is already accepted')
            record.status = 'Accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'Offer Accepted'
            record.property_id.selling_price = record.price

    def action_reject(self):
        for record in self:
            if record.status == 'Refused':
                raise exceptions.UserError('The offer is already rejected')
            if record.status == 'Accepted':
                record.property_id.buyer_id = False
                record.property_id.selling_price = 0
            record.status = 'Refused'

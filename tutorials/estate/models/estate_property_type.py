from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'A catagory for real estate types'

    _sql_constraints = [('unique_name', 'UNIQUE(name)', 'The type name must be unique')]
    _order = 'sequence, name desc'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)

    property_ids = fields.One2many('estate.property', 'estate_property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')

    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

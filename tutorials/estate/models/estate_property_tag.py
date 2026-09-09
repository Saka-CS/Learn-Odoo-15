from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tags that are used to descripe estate properties'

    _sql_constraints = [('unique_name', 'UNIQUE(name)', 'The tag name must be unique')]
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()

    estate_property_ids = fields.Many2many('estate.property', string='Estate Property')

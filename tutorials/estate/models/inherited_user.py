from odoo import models
from odoo.fields import One2many


class InheritedUser(models.Model):
    _inherit = 'res.users'

    estate_property_ids = One2many(
        'estate.property', 'seller_id', string='Properties', domain=[('state', 'in', ['New', 'Offer Received'])]
    )

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.osv import expression
from random import randint


class ProductTag(models.Model):
    _name = 'mad.product.tag'
    _description = 'Product tags'
    _order = 'name'
    _parent_order = 'name'
    _parent_store = True

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Tag Name', required=True, translate=True)
    active = fields.Boolean(
        help='The active field allows you to hide the tag without removing it.',
        default=True,
    )

    color = fields.Integer(string='Renk seçimi', default=_get_default_color)
    image = fields.Binary(string='Resim')

    parent_id = fields.Many2one(string='Parent Tag', comodel_name='mad.product.tag', index=True, ondelete='cascade')
    child_ids = fields.One2many(string='Child Tags', comodel_name='mad.product.tag', inverse_name='parent_id')
    parent_path = fields.Char(index=True)

    """@api.constrains("parent_id")
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_("You cannot create recursive product tags."))

    def name_get(self):
        res = []

        for category in self:
            names = []
            current = category

            while current:
                names.append(current.name)
                current = current.parent_id

            res.append((category.id, " / ".join(reversed(names))))

        return res

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []

        if name:
            parent_ids = []
            parent_domain = []

            for tag in map(lambda t: t.strip(), name.split("/")):
                name_domain = expression.AND([[("name", operator, tag)], parent_domain])
                parent_ids = self._search(
                    name_domain, limit=limit, access_rights_uid=name_get_uid
                )
                parent_domain = [("parent_id", "in", parent_ids)]

            browse_domain = expression.OR([[("id", "in", parent_ids)], parent_domain])
            args = expression.AND([browse_domain, args])

        tag_ids = self._search(args, limit=limit, access_rights_uid=name_get_uid)

        return self.browse(tag_ids).name_get()"""

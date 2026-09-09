from odoo import models, fields


class Template(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template özelleştirmeleri'
    gtipno = fields.Char('GTİP No')
    tag_ids = fields.Many2many(
        string='Tags',
        comodel_name='mad.product.tag',
        relation='product_mad_product_tag_rel',
        ondelete='restrict',
        help='Ürün ve hizmetleri gruplamak için etiket kullanabilirsiniz',
    )

    # kart view'ını iki modelden de açtığımız için ikisinde de bu action mevcut(hem template hem product'tan açıyoruz)
    def action_gtip_no_linki(self):
        if self.id:
            return {
                'type': 'ir.actions.act_url',
                'url': 'https://uygulama.gtb.gov.tr/Tara',
                'target': 'new',
            }

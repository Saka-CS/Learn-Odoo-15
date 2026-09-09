{
    'name': 'mad',
    'version': '1.0',
    'description': 'MAD Odoo için menü ve view özelleştirmeleri',
    'author': 'Deniz Akın',
    'installable': True,
    'license': 'LGPL-3',
    'version': '15.0.1',
    'depends': ['base', 'product', 'stock', 'sale', 'purchase'],
    'data': [
        'views/mad_template_tree_view.xml',
        'views/mad_product_form_view.xml',
        'views/mad_product_tree_view.xml',
        'views/mad_product_menu.xml',
        'views/mad_product_tag_views.xml',
    ],
}

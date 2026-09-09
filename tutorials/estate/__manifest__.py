{
    'name': 'Real Estate App',
    'category': 'Apps',
    'application': True,
    'depends': ['base_setup'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/inherited_user.xml',
        'views/estate_menus.xml',
    ],
}

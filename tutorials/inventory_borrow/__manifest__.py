{
    'name': 'Employee Inventory Borrowing',
    'version': '15.0.1.0.0',
    'summary': 'Allow employees to borrow inventory items',
    'author': 'saka404',
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'depends': ['stock', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/borrow_request.xml',
    ],
}

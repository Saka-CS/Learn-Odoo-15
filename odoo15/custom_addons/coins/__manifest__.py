{
    'name': 'coins',
    'version': '1.0',
    'description': 'Easy Coin Trading',
    'author': 'Deniz Akın',
    'installable': True,
    'license': 'LGPL-3',
    'version': '14.0.1',
    'depends': ['base'],
    'data': [
        'views/coin.xml',
        'views/exchange.xml',
        'views/exchange_api.xml',
        'views/portfolio.xml',
        'views/portfolio_row.xml',
    ],
    # This demo data files will be loaded if db initialize with demo data (commented because file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],
}

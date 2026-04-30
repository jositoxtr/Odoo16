{
    'name': 'Real Es-tate Theme',
    'description': 'Custom waterproof drone e-commerce theme',
    'category': 'Theme/Ecommerce',
    'version': '1.0',
    'author': 'JL',
    'license': 'LGPL-3',  # <--- Añadida la licencia
    'depends': ['website', 'estate'],
    'data': [
        'views/layout.xml',
        'views/snippets.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'theme_RE/static/src/scss/primary_variables.scss',
        ],
        'web.assets_frontend': [
            'https://googleapis.com',
            'theme_RE/static/src/scss/style.scss',
        ],
    },
}


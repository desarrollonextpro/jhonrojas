# -*- coding: utf-8 -*-

{
    'name': 'account massive import transport',
    'version': '13.1.1.0.0',
    'author': 'Jhon',
    'website': '',
    'summary': 'Extencion de algunas funcionalidades de account',
    'description': """ Este módulo extiende las funcionalidades del módulo account 
                        cargandole informacion masiva en la factura""",
    'depends': [
        'stock', 'account'
    ],
    'data': [

        'views/account_move_views.xml',
        'views/account_move_import_drivin_wizard.xml',
    ],
    'installable': True,
    'auto_install': False
}

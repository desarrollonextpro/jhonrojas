{
    'name': 'Prestamos',
    'version': '1.0',
    'description': 'Loan for clients',
    'author': 'Jhon Jairo Rojas Ortiz',
    'license': 'LGPL-3',
    'depends': [
        'base', 'account'
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir_model_access.xml',
        'views/loan.xml'
    ],
    'auto_install': False,
    'application': False,
}

{
    'name': 'Custom Sale',
    'version': '1.0',
    'description': 'custom sale',
    'author': 'Jhon Jairo Rojas Ortiz',
    'license': 'LGPL-3',
    'depends': [
        'sale', 'base_automation', 'project', 'purchase'
    ],
    'data': [
        'security/ir_model_access.xml',
        'data/base_automation.xml',
        'report/purchase_order_template.xml',
        'views/transfer_type.xml',
        'views/sale.xml'
    ],
    'auto_install': False,
    'application': False,

}

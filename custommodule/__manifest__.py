# -*- coding: utf-8 -*-
{
    'name': "Custom-Module",

    'summary': "Custom module",

    'description': "Custom module",

    'author': "Next-pro",
    'website': "http://www.nextpro.pe",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'application': True,
    'version': '0.1',
    'images': [
    ],

    # any module necessary for this one to work correctly
    'depends': ['base', "sale", "website", "website_sale", "nextconnector", "website_sale_delivery", "product"],

    # always loaded
    'data': [
        # vistas de formulario/ listas
        'views/website_sale.xml',
        'views/special_category_view.xml',
        'views/portal.xml',
        'views/website_sale_quick_add.xml',
        'views/res_partner_view.xml',
        'views/product_template_view.xml',
        'views/website_sale_customer_balance.xml',
        # 'views/website_sale_b2b.xml',
        'data/custommodule_identification_type_data.xml',
        'views/website_sale_status_shipping.xml',
        'views/custom_quote_views.xml',
        'views/sale_order_view.xml',
        'views/website_sale_quote.xml',
        'views/website_sale_url_afiliado.xml',
        'views/website_show_view.xml',
        'views/b2b_payment_confirm.xml',
        'templates/website_sale_wishlist_templates.xml',


        # data

        # seguridad
        'security/ir.model.access.csv'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'auto_install': True
}

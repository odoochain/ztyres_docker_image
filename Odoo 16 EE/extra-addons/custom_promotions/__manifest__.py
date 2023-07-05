# -*- coding: utf-8 -*-
{
    'name': "custom_promotions",
    'summary': "Short (1 phrase/line) summary of the module's purpose, used as subtitle on modules listing or apps.openerp.com",
    'description': "Long description of module's purpose",
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['sale', 'account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}

# -*- coding: utf-8 -*-
{
    'name': "Aprobación de Ventas",

    'summary': """
        Módulo para realizar confirmación en varios pasos""",

    'description': """
        Long description of module's purpose
    """,

    'author': "José Roberto Mejía Pacheco,ZTYRES",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/stock_views.xml',
        'views/sale_views.xml',
        
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

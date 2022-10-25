# -*- coding: utf-8 -*-
{
    'name': "Modificaciones de Contabilidad",

    'summary': """
        Se agregaron en este módulo algunas personalizaciones del módulo nativo de Odoo
        account.
        """,

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
    'depends': ['account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/parameter_reset_invoice_sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

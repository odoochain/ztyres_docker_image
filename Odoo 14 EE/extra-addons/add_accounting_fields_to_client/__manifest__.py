# -*- encoding: utf-8 -*-
#
# Module written to Odoo, Open Source Management Solution


{
    'name': 'Add Accounting Field to Clients',
    'author': 'QUEMARI ©',
    'category': 'Invoices',
    'sequence': 50,
    'summary': "Se agregan los campos de factura: uso, metodo de pago y forma de pago.",
    "version": "14.0.1.1.0",
    'website': 'https://www.quemari.com',
    'version': '1.0',
    'description': """
Se agregan los campos de factura: uso, metodo de pago y forma de pago
==============

    """,
    'depends': [
        'account',
        'account_accountant',
        'l10n_mx_edi'
    ],
    'data': [
        'views/res_partner.xml'
    ],
    'demo': [],
    'qweb': [],
    'application': False,
    'installable': True
}

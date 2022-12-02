# -*- coding: utf-8 -*-

{
    'name': "Reporte de Dirección (Dir Report)",
    'summary': """
    Módulo para el reporte de dirección
    """, 
    'category': "Inventory",
    'author' : "Quemari developers",
    'website': "http://www.quemari.com",
    'installable': True, 
    'depends': [
        'stock'
    ],
    'data': [
        'security/ir.model.access.csv',

        'report/dir_report_view.xml',
    ],
}
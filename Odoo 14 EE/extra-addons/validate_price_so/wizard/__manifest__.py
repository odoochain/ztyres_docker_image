# -*- coding: utf-8 -*-

{
    'name': "Validar precio de pedido contra lista de precios",
    'summary': """
    Valida el precio al momento de confirmar el pedido y se pregunta si quiere actualizar o no, en caso de ser necesario
    """,
    'category': "Sales",
    'installable': True, 
    'depends': [
        'stock', 
        'sale_management'
    ],
    'data': [
        'security/ir.model.access.csv',

        'wizard/ask_to_update_prices_so_wizard.xml'
    ],
}
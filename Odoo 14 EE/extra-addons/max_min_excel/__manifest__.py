# -*- coding: utf-8 -*-

{
    'name' : "Subir plantilla para máximos y mínimos", 
    'summary' : """
    Módulo que permite subir una plantilla para máximos y mínimos de productos
    """ , 
    'category' : "Inventory", 
    'author' : "Quemari developers",
    'website' : "http://www.quemari.com", 
    'installable' : True, 
    'depends' : [
        'stock'
    ], 
    'data' : [
        'security/ir.model.access.csv', 

        'views/import_product_min_max_wizard.xml'
    ]
}
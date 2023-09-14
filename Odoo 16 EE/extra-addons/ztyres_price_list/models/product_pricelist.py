# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'
    exclude_from_sale = fields.Boolean(string='Excluir de los precios de ventas',default=True)
    exclude_from_export_lists = fields.Boolean(string='Excluir de la exportación de listas de precios.',default=True)
    

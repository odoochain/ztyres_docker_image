# -*- coding: utf-8 -*-
from odoo import models, fields,api

class Product(models.Model):
    _inherit = 'product.product'

    dot_range = fields.Char(compute='_compute_dot_range', string='DOT')

    # show_sale_line = fields.Boolean(compute='_compute_show_sale_line', string='Mostrar en Línea de Pedido',store=True)
    
    

    # def _compute_show_sale_line(self):
    #     for line in self:
    #         pricelist_item = self.env['product.pricelist.item']
    #         pricelist_items = pricelist_item.search([('pricelist_id','in',[line.order_id.pricelist_id.ids]),('product_tmpl_id','in',line.product_id.product_tmpl_id.ids)])
    #         if pricelist_items:
    #             return 1
    #         else:
    #             return 0
    def _compute_dot_range(self):
        product_lot = self.env['stock.lot']
        for record in self:
            record.dot_range = 'N/A'
            lots = product_lot.search([('product_id','in',[record.id])]).mapped('name')
            if lots:
                try:
                    arr_dict = []
                    for item in lots:                    
                        if len(item)==4:
                            arr_dict.append((int(item[-2:]),int(item[:2])))
                        elif len(item)==3:
                            arr_dict.append((int(item[-2:]),int(item[:1])))
                    sorted_list_year_month = sorted(arr_dict)
                    max_dot = str(sorted_list_year_month[-1][1])+str(sorted_list_year_month[-1][0])
                    min_dot = str(sorted_list_year_month[0][1])+str(sorted_list_year_month[0][0])
                    if max_dot == min_dot:
                        record.dot_range = '%s'%(max_dot)
                    else:
                        record.dot_range = '%s-%s'%(min_dot,max_dot)
                except Exception as e:
                    print('Error de DOT en producto')
                    record.dot_range = 'N/A'
            else:
                record.dot_range = 'N/A'

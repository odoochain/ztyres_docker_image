from odoo import _, api, fields, models


class Product(models.Model):
    _inherit = 'product.product'

    dot_range = fields.Char(compute='_compute_dot_range', string='Dot Máximo y Mínimo')

    def _compute_dot_range(self):
        product_lot = self.env['stock.production.lot']
        for record in self:
            lots = product_lot.search([('product_id','in',[record.id])]).mapped('name')
            if lots:
                if len(lots)>0:
                    for i in range(0, len(lots)):
                        lots[i] = int(lots[i])
                    record.dot_range = '%s-%s'%(max(lots),min(lots))
                else:
                    record.dot_range = '%s'%(lots)[0]
            else:
                record.dot_range = 'N/A'

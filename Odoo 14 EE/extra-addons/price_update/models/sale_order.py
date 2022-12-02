# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import logging 
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model): 
    _inherit = 'sale.order'

    def update_sale_order_prices(self): 
        for order in self.search([('state', '=', 'sale')]):
            for category in order.partner_id.category_id:
                if category.id in (4, 6, 8): 
                    order.update_prices()
    
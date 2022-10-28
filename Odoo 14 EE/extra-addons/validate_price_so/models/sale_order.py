# -*- coding: utf-8 -*-

from itertools import product
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model): 
    _inherit = 'sale.order'


    def action_confirm(self, ignore=False):
        if ignore == False:
            for item in self.pricelist_id.item_ids:
                for order_line in self.order_line:
                    if order_line.product_id.product_tmpl_id == item.product_tmpl_id and order_line.price_unit != item.fixed_price: 
                        return {
                            'view_mode' : 'form', 
                            'type' : 'ir.actions.act_window',
                            'res_model' : 'ask.to.update.prices.so',
                            'target' : 'new',
                            'view_id' : self.env.ref('validate_price_so.ask_to_update_prices_so_wizard_view').id,
                            'context' : {'order_id' : self.id}
                        }
                
        return super(SaleOrder, self).action_confirm()
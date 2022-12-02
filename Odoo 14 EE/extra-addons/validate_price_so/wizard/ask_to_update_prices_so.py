# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import logging
_logger = logging.getLogger(__name__)

class AskToUpdatePricesSo(models.TransientModel):
    _name = 'ask.to.update.prices.so'

    def confirm(self):
        self.env['sale.order'].search([('id', '=', self._context['order_id'])]).action_confirm(True)

    def update(self): 
        self.env['sale.order'].search([('id', '=', self._context['order_id'])]).update_prices()
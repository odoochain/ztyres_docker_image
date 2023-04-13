# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from datetime import datetime
from odoo.exceptions import UserError

class ChooseDeliveryCarrier(models.TransientModel):
    _inherit = 'choose.delivery.carrier'
    _description = 'Delivery Carrier Selection Wizard'
    display_price = fields.Float(string='Cost', readonly=False)
    
    
    def button_confirm(self):
        self.order_id.set_delivery_line(self.carrier_id, self.display_price)
        self.order_id.write({
            'recompute_delivery_price': False,
            'delivery_message': self.delivery_message,
        })

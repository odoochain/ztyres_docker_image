# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models,fields

class StockPicking(models.Model):
    _inherit = ['stock.picking']

    

    def action_cancel(self):
        # if self.state_sale_id:
        #     self.state_sale_id = 'cancel'
        result = super(StockPicking, self).action_cancel()
        return result
    
    def separation_status_done(self):
        for rec in self:
            rec.separation_status='done'

    def separation_status_draft(self):
        for rec in self:
            rec.separation_status='draft'
    
    def button_validate(self):
        if self.location_dest_id.id in self.env['stock.location'].search([('complete_name','ilike','WH')]).ids:
            self.scheduled_date = fields.Datetime.now()            
        return super(StockPicking, self).button_validate()
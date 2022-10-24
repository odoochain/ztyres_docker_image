# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Sale(models.Model):
    _inherit = 'sale.order'
    APPROVE_STATES = [('draft', 'Gerente de Ventas'),('done', 'Crédito y Cobranza'),('confirm', 'Anticipado')]
    approve_state = fields.Selection(string='Estado de Aprobación', selection=APPROVE_STATES,track_visibility='onchange')
    SHIPMENT_STATES = [('draft', 'Solicitud de Embarques No Aprobada'),('done', 'Solicitud de Embarques Aprobada')]
    shipment_state = fields.Selection(string='Solicitud de Embarque', selection=SHIPMENT_STATES,track_visibility='onchange',default='draft')

    def sale_approve_state_draft(self):
        for record in self:
            record.approve_state = 'draft'

    def sale_approve_state_done(self):
        for record in self:
            record.approve_state = 'done'

    def sale_approve_state_confirm(self):
        for record in self:
            record.approve_state = 'confirm'

    def sale_shipment_state_draft(self):
        for record in self:
            record.shipment_state = 'draft'

    def sale_shipment_state_done(self):
        for record in self:
            record.shipment_state = 'done'   

    #  = fields.Integer(related='payment_term_id.days', string='Días de Crédito')
    
    payment_term_days = fields.Integer(compute='_compute_payment_term_days',string='Días de Crédito')
    
    
    def _compute_payment_term_days(self):
        for record in self:
            print(record.payment_term_id.line_ids.days)
            self.payment_term_days = record.payment_term_id.line_ids.days
        
    

    
    
# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class Sale(models.Model):
    _inherit = 'sale.order'
    APPROVE_STATES = [('draft', 'Gerente de Ventas'),('done', 'Crédito y Cobranza'),('confirm', 'Anticipado')]
    approve_state = fields.Selection(string='Estado de Aprobación', selection=APPROVE_STATES,track_visibility='onchange')
    SHIPMENT_STATES = [('draft', 'Solicitud de Embarque No Aprobada'),('done', 'Solicitud de Embarque Aprobada')]
    shipment_state = fields.Selection(string='Solicitud de Embarque', selection=SHIPMENT_STATES,track_visibility='onchange',default='draft')
    payment_term_days = fields.Integer(compute='_compute_payment_term_days',string='Días de Crédito')

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
            for picking in record.picking_ids:
                picking.shipment_state = record.shipment_state       


    def sale_shipment_state_done(self):
        for record in self:
            record.shipment_state = 'done'  
            for picking in record.picking_ids:
                picking.shipment_state = record.shipment_state         
    
    def _compute_payment_term_days(self):
        for record in self:
            record.payment_term_days = record.payment_term_id.line_ids.days

    ready_to_shipment_validation = fields.Boolean(compute="_compute_ready_to_shipment_validation", help="Whether or not this line should display a button allowing to remove its related payments from the batch")

    def _compute_ready_to_shipment_validation(self):
        for record in self:
            result = False
            if record.payment_term_days>0 and record.approve_state=='done' and record.shipment_state not in ['done']:
                result = True
            elif record.payment_term_days==0 and record.approve_state=='confirm' and record.shipment_state not in ['done']:
                result = True                     
            record.ready_to_shipment_validation = result

    def action_confirm(self):
        if self.shipment_state not in ['done']:
            raise ValidationError(_("Necesita tener la Aprobación de Embarque para poder ser confirmada."))
        return super(Sale, self).action_confirm()



    


    
    
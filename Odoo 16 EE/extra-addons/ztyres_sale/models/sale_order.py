# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from datetime import datetime
from odoo.exceptions import UserError
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_id_total_due = fields.Monetary(related='partner_id.total_due',string='Adeudo Total',store=False)
    partner_id_credit_available = fields.Monetary(compute='_credit_available',string='Cŕedito disponible',store=False)
    partner_id_total_overdue = fields.Monetary(related='partner_id.total_overdue',string='Adeudo Vencido', store=False)
    partner_id_unpaid_invoices_count = fields.Integer(related='partner_id.unpaid_invoices_count',string='Cantidad de facturas sin pagar',store=False)
    partner_id_csf = fields.Char(related='partner_id.csf', store=False,string = 'Cosntancia de situacion fiscal')
    payment_term_days = fields.Integer(compute='_compute_payment_term_days',string='Días de Crédito')
    show_partner_credit_alert = fields.Boolean(compute='_compute_show_partner_credit_alert')
    grant_overdue_credit = fields.Selection(string='Sobre giro de cuenta', selection=[ ('unlocked', 'Venta con sobregiro consentido')],default=False)
    not_change_price = fields.Boolean('No cambiar precio',default=False)
    def _compute_payment_term_days(self):
        for record in self:
            record.payment_term_days = record.payment_term_id.line_ids.days
    
    def _compute_show_partner_credit_alert(self):
        for order in self:
            order.show_partner_credit_alert = True
    
    def set_unlock_overdue_credit(self):
        self.grant_overdue_credit = 'unlocked'
        display_msg = """ Venta con sobregiro aprobada """"""
              <br/>               
              """"""
              <br/>
              <b></b>
              <br/>
          """      
        self.message_post(body=display_msg)        
        
    def set_lock_overdue_credit(self):
        self.grant_overdue_credit = False

#TODO: Doesn't works.


    def get_account_report(self):
        return self.env.ref('studio_customization.studio_report_docume_a799a671-df55-4ef3-9f6e-1c6cd7e7cdbb').report_action(self.partner_id)

    def action_confirm(self):
        for order in self:
            if order.grant_overdue_credit !='unlocked':
                order.check_account_lock()      
                order.check_credit_available()
        return super(SaleOrder, self).action_confirm()
    
    def check_account_lock(self):
        for order in self:            
            if order.partner_id.total_overdue>0:
                raise UserError('Presenta saldo vencido, por favor comuníquese con el área de Finanzas') 
    
    def _credit_available(self):
        for order in self:
            available = order.partner_id.credit_limit - order.partner_id.total_due
            if available <=0:
                if order.partner_id.credit_limit > 0:
                    available = abs(available)
                else:
                    available = 0
            order.partner_id_credit_available = available
            return available
        
        
    def check_credit_available(self):
        for order in self:                                           
            if not order.partner_id_credit_available >= order.amount_total:
                raise UserError('Esta cotización excede el límite de crédito del cliente, por favor comuníquese con el área de Finanzas') 
# -*- coding: utf-8 -*-
from odoo import models, fields
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
    grant_overdue_credit = fields.Selection(string='Sobre giro de cuenta', selection=[ ('unlocked', 'Venta con sobregiro consentido')],default=False,copy=False)
    not_change_price = fields.Boolean('No cambiar precio',default=False)
    payment_receipts_count = fields.Integer(compute='_compute_payment_receipts_count', string='Comprobantes de pago')
   
    
    def _compute_payment_receipts_count(self):
        self.payment_receipts_count = 3
    
    
    def open_payment_receipts(self):
        pass
    
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

    def write(self, values):
        res = super().write(values)        
        if values.get("order_line") is not None:
            self.quotation_action_confirm()                                                  
        return res
    
    
    def action_confirm(self):
        for order in self:
            if order.grant_overdue_credit !='unlocked':
                order.check_account_lock()      
                order._check_credit_available()
                order.x_studio_val_ventas = True                
                order.x_studio_val_credito = True
                order.x_studio_val_pago = True
                order.x_studio_solicitud_de_embarques = 'Si'
            order.x_studio_val_ventas = True                
            order.x_studio_val_credito = True
            order.x_studio_val_pago = True
            order.x_studio_solicitud_de_embarques = 'Si'                
        return super(SaleOrder, self).action_confirm()
    
    def check_account_lock(self):
        for order in self:            
            if order.partner_id.total_overdue>0:
                raise UserError('Presenta saldo vencido, por favor comuníquese con el área de Finanzas') 
    
    def _credit_available(self):
        for order in self:
            available = order.partner_id.credit_limit - order.partner_id.total_due
            if available <= 0:
                if order.partner_id.credit_limit > 0:
                    available = abs(available)
                else:
                    available = 0
            order.partner_id_credit_available = available
            return available
        
        
    def _check_credit_available(self):
        for order in self:                                                 
            if not order.partner_id_credit_available >= order.amount_total:
                raise UserError('Esta cotización excede el límite de crédito del cliente, por favor comuníquese con el área de Finanzas')
            forecast_used = self.forecast_used_credit()
            if not order.partner_id_credit_available >= order.amount_total + forecast_used:
                message = 'Esta cotización excede el límite de cŕedito previsto: Disponible %s Previsto %s'%(order.partner_id_credit_available,forecast_used)
                raise UserError(message)            
            
    
    def forecast_used_credit(self):
        domain = []
        states = ['cancel','draft']
        domain.append(('partner_id','in',self.partner_id.ids))
        domain.append(('state','not in',states))
        invpoice_states = ['invoiced']
        domain.append(('invoice_status','not in',invpoice_states))
        return sum(self.search(domain).mapped('amount_total'))

    def action_draft(self):
        for order in self:            
            order.quotation_action_confirm()       
        return super(SaleOrder, self).action_draft()    
    

    def quotation_action_confirm(self):     
        # Validate sale policies again
        for order in self:            
            for picking in order.picking_ids:
                if picking.x_studio_embarque:
                    raise UserError('No se pueden modificar cantidades en un traslado %s embarcado %s'%(picking.name,picking.x_studio_embarque.x_name))                                
                if picking.state not in ['done']:
                    picking.do_unreserve()
                    picking.action_cancel()
                    picking.sudo().unlink()

        self.order_line._ztyres_action_launch_stock_rule()

    def _action_cancel_delete_picking_ids(self):
        res = super(SaleOrder, self).action_cancel()
        for order in self:    
            for picking in order.picking_ids:
                if picking.state in ['cancel']:
                    picking.sudo().unlink()     
        return res

    def action_cancel(self):
        self._action_cancel_delete_picking_ids()
        self.with_context(tracking_disable=True)._action_cancel()     
        self.message_post(body="Cancelado") 
        self.grant_overdue_credit = False  
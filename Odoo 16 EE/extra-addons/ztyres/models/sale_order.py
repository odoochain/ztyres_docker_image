# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from datetime import datetime
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from odoo.tools import (
    formatLang,

)
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    partner_credit_limit_used = fields.Monetary(related='partner_id.credt_limit_used', readonly=True)
    partner_credit_limit_available = fields.Monetary(related='partner_id.credt_limit_available', readonly=True)    
    show_partner_credit_alert = fields.Boolean(compute='_compute_show_partner_credit_alert')
    partner_credit_limit = fields.Float(related='partner_id.credit_limit', readonly=True)
    partner_credit_amount_overdue = fields.Monetary(related='partner_id.credit_amount_overdue', readonly=True)
    sale_reason_cancel_id = fields.Many2many(comodel_name='ztyres.sale_reason_cancel', string='Motivo de Cancelación')
    payment_term_days = fields.Integer(compute='_compute_payment_term_days',string='Días de Crédito')
    keep = fields.Boolean(string='Mantener Pedido de Venta', default=False)
    unlock_financial = fields.Boolean(string='Excepcion de pedido', default=False)
    pricelist_locked = fields.Boolean(string="Lista de precios bloqueada", default=False)

    @api.onchange('pricelist_id')
    def _check_pricelist_locked(self):
        # Si pricelist_locked es True, entonces se ha establecido una lista de precios anteriormente
        if self.pricelist_locked:
            # Se restaura el valor anterior para prevenir el cambio
            self.pricelist_id = self._origin.pricelist_id
            return {
                'warning': {
                    'title': _("Advertencia!"),
                    'message': _("Una vez seleccionada, no puedes cambiar la lista de precios, se restaurará a la lista seleccionada inicialmente."),
                }
            }
        else:
            # Se bloquea la lista de precios para futuros cambios
            self.pricelist_locked = True

    def _prepare_invoice(self):
        # Llamamos al método original para obtener el diccionario preparado
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        # Copiamos los términos y condiciones del pedido de venta a la factura
        invoice_vals['narration'] = self.note  # Asumiendo que `note` es el campo de términos y condiciones en sale.order
        return invoice_vals
    
    allowed_product_ids = fields.Many2many(
        'product.product', 
        compute='_compute_allowed_product_ids', 
        store=False
    )


    @api.depends('pricelist_id')
    def _compute_allowed_product_ids(self):
        for order in self:
            items = order.pricelist_id.item_ids.product_tmpl_id.mapped('product_variant_id')
            services = self.env['product.product'].search([('id','in',[50959])])
            order.allowed_product_ids = services + items

    def copy(self, default=None):
        # Agregar codigo de validacion aca
        raise UserError(_('No es posible duplicar un pedido de Venta'))
        

    def _lock_credit_warning_message(self,updated_credit):
        ''' Build the warning message that will be displayed in a yellow banner on top of the current record
            if the partner exceeds a credit limit (set on the company or the partner itself).
            :param record:                  The record where the warning will appear (Invoice, Sales Order...).
            :param updated_credit (float):  The partner's updated credit limit including the current record.
            :return (str):                  The warning message to be showed.
        '''
        partner_id = self.partner_id.commercial_partner_id
        if not partner_id.credit_limit or updated_credit <= partner_id.credit_limit:
            return ''
        msg = _('%s se alcanzó el límite de crédito de : %s\nTotal adeudado ',
                partner_id.name,
                formatLang(self.env, partner_id.credit_limit, currency_obj=self.company_id.currency_id))
        if updated_credit > partner_id.credit:
            msg += _('(incluido este documento) ')
        msg += ': %s' % formatLang(self.env, updated_credit, currency_obj=self.company_id.currency_id)
        raise UserError(msg)
    

    def _onchange_check_customer_invoices(self):
        if not self.partner_id.total_overdue <= 0.0:
            raise UserError(_('Este cliente tiene facturas vencidas. $ %s Por favor, verifica su situación antes de proceder con el pedido de venta.'%(str(self.partner_id.total_overdue))))


    def cancel_old_quotation_picking(self):
        today = fields.Date.today()
        five_days_ago = today - timedelta(days=5)
        # Encuentra los pedidos que están en estado 'cotización' y tienen más de 5 días desde su creación
        old_quotations = self.search([
            ('state', 'in', ['draft']),('keep', '!=',True),
            ('create_date', '<=', five_days_ago)
        ])
        for order in old_quotations:
            # Cancela los documentos relacionados de stock.picking
            try:
                order.picking_ids.action_cancel()
            except:
                print('Error')
                
    def sale_approve_state_draft(self):
        for record in self:
            record.approve_state = 'draft'



    def sale_approve_state_confirm(self):
        for record in self:
            record.approve_state = 'confirm'            


    def _compute_payment_term_days(self):
        for record in self:
            record.payment_term_days = record.payment_term_id.line_ids.days


    def _compute_show_partner_credit_alert(self):
        for order in self:
            order.show_partner_credit_alert = True

    def _action_cancel_delete_picking_ids(self):
        res = super(SaleOrder, self).action_cancel()
        for order in self:    
            for picking in order.picking_ids:
                if picking.state in ['cancel']:
                    picking.sudo().unlink()     
        return res

    @api.model
    def create(self, values):        
        result = super().create(values)
        result.quotation_action_confirm()
        
        return result
    
    
    def write(self, values):       
        res = super().write(values)        
        if values.get("order_line") is not None:
            # self.order_line.check_price_not_in_zero()
            if self.state == 'done':
                self.action_unlock()
            if self.state == 'draft':
                self.quotation_action_confirm()                                        
        return res
    
    @api.onchange('order_line')
    def validate_same_pricelist(self):
        if self.order_line:
            price_list_ids = self.order_line.mapped("pricelist_id").ids
            if not all(x == price_list_ids[0] for x in price_list_ids):
                raise UserError("Las líneas del pedido no corresponden a la misma lista de precio, por favor verifiquelas.")
            if price_list_ids[0] != self.pricelist_id.id:
                raise UserError("Las líneas del pedido no corresponden a la misma lista de precio, por favor verifiquelas.")
        
    

    @api.onchange('pricelist_id')
    def onchange_pricelist_id(self):
        self.note = self.pricelist_id.terms

    def action_confirm(self):
        #TODO Check this validation
        

        if not self.payment_term_days > 0:
            if not self.x_studio_val_pago:
                raise UserError("Por favor verifique con finanzas el pago anticipado.")
        updated_credit = self.partner_id.commercial_partner_id.credit + (self.amount_total * self.currency_rate)
        if not self.unlock_financial:
            self._onchange_check_customer_invoices()
            self._lock_credit_warning_message(updated_credit)
        self.x_studio_val_credito =True
        self.x_studio_val_ventas = True
        self.x_studio_solicitud_de_embarques = 'Si'
        return super(SaleOrder, self).action_confirm()

    def action_draft(self):
        for order in self:            
            order.quotation_action_confirm()       
        return super(SaleOrder, self).action_draft()    

    def quotation_action_confirm(self):     
        # Validate sale policies again
        for order in self:            
            for picking in order.picking_ids:
                if picking.state not in ['done']:
                    picking.do_unreserve()
                    picking.action_cancel()
                    picking.sudo().unlink()

        self.order_line._ztyres_action_launch_stock_rule()

    def _ztyres_account_status(self):
        unpaid_invoices = False
        balance_for_followup = False
        for order in self:
            unpaid_invoices = order.partner_id._ztyres_compute_unpaid_invoices()
            balance_for_followup = order.partner_id._ztyres_compute_for_followup() 
        return (unpaid_invoices,balance_for_followup)
    


    def action_cancel(self):
        self.x_studio_val_credito =False
        self.x_studio_val_pago =False
        self.x_studio_val_ventas = False
        self.x_studio_solicitud_de_embarques = False
        return {
            'type': 'ir.actions.act_window',
            'name': 'Motivo de Cancelación',
            'res_model': 'ztyres.cancel_reason',
            'view_mode': 'form',            
            'target': 'new',
            'context' : {'sale_id':self}
        }


# -*- coding: utf-8 -*-
from odoo import models, fields, api

class account_move(models.Model):
    _inherit = 'account.move'
    generic_edi = fields.Boolean("Timbrado genérico")
    def button_process_edi_web_services(self):
        #TODO change direct id 8606 by selection or parameter.
        if self.generic_edi:            
            current_partner = self.partner_id.id
            self.l10n_mx_edi_usage = 'S01'
            self.partner_id = 8625
            result = super(account_move, self).button_process_edi_web_services()
            self.partner_id = current_partner        
            return result
        else:
            result = super(account_move, self).button_process_edi_web_services()
            return result
            

    def action_retry_edi_documents_error(self):
        #TODO change direct id 8606 by selection or parameter.
        if self.generic_edi:            
            current_partner = self.partner_id.id
            self.l10n_mx_edi_usage = 'S01'
            self.partner_id = 8625
            result = super(account_move, self).action_retry_edi_documents_error()
            self.partner_id = current_partner        
            return result
        else:
            result = super(account_move, self).action_retry_edi_documents_error()
            return result
            
                

        



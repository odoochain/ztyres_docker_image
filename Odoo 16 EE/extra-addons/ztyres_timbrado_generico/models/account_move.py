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

    def action_process_edi_web_services(self, with_commit=True):
        docs = self.edi_document_ids.filtered(lambda d: d.state in ('to_send', 'to_cancel') and d.blocking_level != 'error')
        docs._process_documents_web_services(with_commit=with_commit)
        if self.l10n_mx_edi_cfdi_uuid and self.is_invoice(include_receipts=True):
            action = self.with_context(discard_logo_check=True).action_invoice_sent()
            action_context = action['context']
            invoice_send_wizard = self.env['account.invoice.send'].with_context(
                action_context,
                active_ids=[self.id]
            ).create({'is_print': False})
            # By default, `mail.mail` are automatically deleted after being sent.
            # This line desables this behavior, ensuring that the record remains
            # available for further testing
            invoice_send_wizard.template_id.auto_delete = False
            invoice_send_wizard.send_and_print_action()
                

        



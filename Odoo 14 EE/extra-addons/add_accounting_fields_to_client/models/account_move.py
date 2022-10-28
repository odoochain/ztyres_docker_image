# -*- encoding: utf-8 -*-
#
# Module written to Odoo, Open Source Management Solution


from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('partner_id')
    def onchange_func(self):
        if self.partner_id:
            self.l10n_mx_edi_usage = self.partner_id.l10n_mx_edi_usage
            self.l10n_mx_edi_payment_method_id = self.partner_id.l10n_mx_edi_payment_method_id


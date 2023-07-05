# -*- coding: utf-8 -*-
from odoo import models, fields,_
from odoo.exceptions import ValidationError, UserError
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    dot_range = fields.Char(related='product_id.dot_range')
    currency_price_subtotal = fields.Float(compute='_compute_currency_price_subtotal', string='Conversión a moneda Local')
    
    def _compute_currency_price_subtotal(self):
        for record in self:
            record.currency_price_subtotal = record.currency_id._convert(record.price_subtotal,record.company_currency_id,record.company_id,record.date)
    
    def _check_reconciliation(self):
        for line in self:
            if line.matched_debit_ids or line.matched_credit_ids:
                pass
                # raise UserError(_("You cannot do this modification on a reconciled journal entry. "
                #                   "You can just change some non legal fields or you must unreconcile first.\n"
                #                   "Journal Entry (id): %s (%s)") % (line.move_id.name, line.move_id.id))
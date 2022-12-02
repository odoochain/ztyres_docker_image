from odoo import _, api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    currency_price_subtotal = fields.Float(compute='_compute_currency_price_subtotal', string='Conversión a moneda Local')
    
    
    def _compute_currency_price_subtotal(self):
        for record in self:
            record.currency_price_subtotal = record.currency_id._convert(record.price_subtotal,record.company_currency_id,record.company_id,record.date)
    

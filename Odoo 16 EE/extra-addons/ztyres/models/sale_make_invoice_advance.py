from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def create_invoices(self):
        raise UserError(_('No es posible realizar una factura de varios pedidos, solicite ayuda a soporte.'))
        # CODE HERE

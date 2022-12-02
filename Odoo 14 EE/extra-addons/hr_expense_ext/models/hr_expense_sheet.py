from odoo import _, api, fields, models


class HrExpense(models.Model):
    _inherit = 'hr.expense.sheet'

    payment_date = fields.Date(string='Fecha en que se pagó.')

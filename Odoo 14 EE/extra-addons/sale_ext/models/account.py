from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    dot_range = fields.Char(related='product_id.dot_range')
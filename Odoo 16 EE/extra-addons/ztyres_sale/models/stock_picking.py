from odoo import _, api, fields, models
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'


    def button_validate(self):
        if self.location_dest_id.id in self.env['stock.location'].search([('complete_name','ilike','WH')]).ids:
            self.scheduled_date = fields.Datetime.now()            
        return super(StockPicking, self).button_validate()

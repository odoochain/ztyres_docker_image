from odoo import _, api, fields, models


class Stock(models.Model):
    _inherit = 'stock.picking'
    SHIPMENT_STATES = [('draft', 'Solicitud de Embarque No Aprobada'),('done', 'Solicitud de Embarque Aprobada')]
    shipment_state = fields.Selection(selection=SHIPMENT_STATES,default='draft',string='Solicitud de Embarque')
    

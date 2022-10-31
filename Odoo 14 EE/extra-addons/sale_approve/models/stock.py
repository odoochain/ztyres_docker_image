from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class Stock(models.Model):
    _inherit = 'stock.picking'
    SHIPMENT_STATES = [('draft', 'Solicitud de Embarque No Aprobada'),('done', 'Solicitud de Embarque Aprobada')]
    shipment_state = fields.Selection(selection=SHIPMENT_STATES,default='draft',string='Solicitud de Embarque')
    sale_is_set = fields.Boolean(compute='_compute_sale_is_set', string='Tiene Cotización ó Pedido de Venta Asociado')
    

    def _compute_sale_is_set(self):
        for record in self:
            if record.sale_id:
                record.sale_is_set = True
            else:
                record.sale_is_set = False
    
    def button_validate(self):
        for record in self:
            if record.sale_is_set:
                if record.shipment_state not in ['done']:
                    raise ValidationError(_("Necesita realizar la confirmación de embarque para poder continuar."))
        return super(Stock, self).button_validate()
    
        

    

    
    
    
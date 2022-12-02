# -*- coding: utf-8 -*-

from odoo import models, fields, _
import openpyxl 
import base64
from io import BytesIO
from odoo.exceptions import UserError
import logging 
_logger = logging.getLogger(__name__)

class ImportProductMinMax(models.TransientModel): 
    _name = 'import.product.min.max'

    file = fields.Binary(string = "Subir archivo de excel", required=True)

    def import_data(self): 
        try: 
            workbook = openpyxl.load_workbook(
                filename = BytesIO(base64.b64decode(self.file)), read_only=True
            )
            worksheet = workbook.active
            for record in worksheet.iter_rows(min_row=2, max_row=None, min_col=None, max_col=None, values_only=True): 
                internal_reference = self.env['product.template'].search([('default_code', '=', record[0])])
                if internal_reference: 
                    location_id = self.env['stock.location'].search([('complete_name', '=', record[1])]).id
                    self.env['stock.warehouse.orderpoint'].create({
                        'product_id'       : internal_reference.product_variant_id.id,
                        'location_id'      : location_id, 
                        'product_min_qty'  : record[2], 
                        'product_max_qty'  : record[3], 
                        'qty_multiple'     : record[4],
                        'product_uom_name' : record[5],
                    })
        except: 
            raise UserError(_('Error al procesar: Es posible que el archivo no se haya leído correctamente a causa de algún dato no reconocido o de haber subido un formato incorrecto'))

            


# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime


    
class PromocionTier(models.Model):
    _name = 'custom_promotions.tier'
    _description = 'Tiers participantes temporales'
    name = fields.Char(string='Nombre')
    clave = fields.Char(string='Clave')

    
    def inserts(self):
        # Ejecutar la consulta SQL
        self.env.cr.execute("""
            SELECT value FROM ir_model_fields_selection
            WHERE field_id IN (
                SELECT id FROM ir_model_fields
                WHERE model = 'product.template' AND name = 'x_studio_posicionamiento'
            )
        """)
        result = self.env.cr.fetchall()

        if result:
            tier_obj = self.env['custom_promotions.tier']
            existing_tiers = tier_obj.search([('name', 'in', [row[0] for row in result])])
            existing_names = existing_tiers.mapped('name')

            # Insertar nuevos registros
            new_tiers = [{'name': row[0]} for row in result if row[0] not in existing_names]
            tier_obj.create(new_tiers)
            
class PromocionMarca(models.Model):
    _name = 'custom_promotions.marca'
    _description = 'Marcas participantes temporales'
    name = fields.Char(string='Nombre')
    clave = fields.Char(string='Clave')


    def inserts(self):
        # Ejecutar la consulta SQL
        self._cr.execute("""
            SELECT value FROM ir_model_fields_selection
            WHERE field_id IN (
                SELECT id FROM ir_model_fields
                WHERE model = 'product.template' AND name = 'x_studio_marca'
            )
        """)
        result = self._cr.fetchall()

        if result:
            marca_obj = self.env['custom_promotions.marca']
            for value in result:
                # Verificar si el registro ya existe
                existing_marca = marca_obj.search([('name', '=', value[0])], limit=1)
                if not existing_marca:
                    # Insertar nuevo registro
                    marca_obj.create({'name': value[0]})

class PromocionMedida(models.Model):
    _name = 'custom_promotions.medida'
    _description = 'Medidas participantes temporales'
    name = fields.Char(string='Nombre')
    clave = fields.Char(string='Clave')

    
    def inserts(self):
        # Ejecutar la consulta SQL
        self.env.cr.execute("""
            SELECT value FROM ir_model_fields_selection
            WHERE field_id IN (
                SELECT id FROM ir_model_fields
                WHERE model = 'product.template' AND name = 'x_studio_medida_1'
            )
        """)
        result = self.env.cr.fetchall()

        if result:
            medida_obj = self.env['custom_promotions.medida']
            existing_medidas = medida_obj.search([('name', 'in', [row[0] for row in result])])
            existing_names = existing_medidas.mapped('name')

            # Insertar nuevos registros
            new_medidas = [{'name': row[0]} for row in result if row[0] not in existing_names]
            medida_obj.create(new_medidas)
#python3 -m ptvsd --host localhost --port 5678 /usr/bin/odoo -d ZTYRES_TEST --config /etc/odoo/odoo.conf --xmlrpc-port=8001 --workers=0

class PromocionPeriodo(models.Model):
    _name = 'custom_promotions.promocion'
    _description = 'Promociones por Periodo'
    _rec_name = 'clave_promocion'
    # Definir la vista de formulario con las columnas personalizadas
    TIPO = [
        ('opcion1', 'Periodo'),
        ('opcion2', 'Entrega')
    ]
    SUMA_POLITICA_COMERCIAL = [
        ('opcion1', 'Si suma a politica comercial'),
        ('opcion2', 'No suma a politica comercial')
    ]
    clave_promocion = fields.Char(string='Clave de Promoción',required=True)
    tier_ids = fields.Many2many('custom_promotions.tier',string='Tiers participantes')
    volumen = fields.Char(string='Volumen')
    terminos_pago_id = fields.Many2many('account.payment.term', string='Términos de Pago')
    porcentaje = fields.Float(string='Porcentaje de descuento en NC')
    promotion_id = fields.Many2one('custom_promotions.promocion', string='Promocion')
    llanta_gratis = fields.Float(string='Llanta de meor precio gratis')
    product_ids = fields.Many2many('product.template', string='Productos Participantes')
    marca_id = fields.Many2many('custom_promotions.marca',string='Marcas participantes')
    medida_id = fields.Many2many('custom_promotions.medida',string='Medidas participantes')
    suma_politica_comercial = fields.Selection(SUMA_POLITICA_COMERCIAL, string='Suma a politicas comeciales', multiple=True)
    fecha_desde = fields.Date(string='Desde', required=True)
    fecha_hasta = fields.Date(string='Hasta', required=True)

    def get_action(self):
        self.marca_id.inserts()
        self.medida_id.inserts()
        self.tier_ids.inserts()
        views = [
                 (self.env.ref('custom_promotions.view_promocion_tree').id, 'list'),
                 (self.env.ref('custom_promotions.view_promocion_form').id, 'form')]
        return{
                'name': 'Promociones por Periodo',
                'view_type': 'form',
                "view_mode": "tree,form",
                #"view_mode": "tree,form,graph",
                'view_id': False,
                "res_model": "custom_promotions.promocion",
                'views': views,
                #'domain': [('id', 'in', invoices.ids)],
                'type': 'ir.actions.act_window',
            }


# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from datetime import datetime
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order' 

    promocion_id = fields.Many2many('custom_promotions.promocion', string='Promocion')
    
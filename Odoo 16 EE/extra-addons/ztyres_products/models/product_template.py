from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    """
    Propiedad de llantas
    """
    tire_measure_id = fields.Many2one('ztyres_products.tire_measure', string='Medida')
    face_id = fields.Many2one('ztyres_products.face', string='Cara')
    layer_id = fields.Many2one('ztyres_products.layer', string='Capas')
    manufacturer_id = fields.Many2one('ztyres_products.manufacturer', string='Fabricante')
    brand_id = fields.Many2one('ztyres_products.brand', string='Marca')
    model_id = fields.Many2one('ztyres_products.model', string='Modelo')
    speed_id = fields.Many2one('ztyres_products.speed', string='Velocidad')
    index_of_load_id = fields.Many2one('ztyres_products.index_of_load', string='Indice de carga')
    wholesale_rebate_id = fields.Many2one('ztyres_products.wholesale_rebate', string='RM')
    country_id = fields.Many2one('res.country', string='Origen')
    segment_id = fields.Many2one('ztyres_products.segment', string='Segmento')
    tier_id = fields.Many2one('ztyres_products.tier', string='Tier')
    type_id = fields.Many2one('ztyres_products.type', string='Tipo')
    supplier_segment_id = fields.Many2one('ztyres_products.supplier_segment', string='Segmento de proveedor')
    original_equipment_id = fields.Many2one('ztyres_products.original_equipment', string='Equipamiento original')
    usage_id = fields.Many2one('ztyres_products.usage', string='Uso')
    e_mark_id = fields.Many2one('ztyres_products.e_mark', string='E-Mark')
    s_mark_id = fields.Many2one('ztyres_products.s_mark', string='S-Mark')
    ccc_id = fields.Many2one('ztyres_products.ccc', string='CCC')
    product_dot_range = fields.Char(compute='_compute_product_dot_range', string='DOT')
    tire = fields.Boolean(string='Es llanta?',tracking=True)
    
    def _compute_product_dot_range(self):
        for record in self:
            record.product_dot_range = record.product_variant_id.dot_range
    
    
    def write(self, values):
        # CODE HERE
        if ['tire_measure_id']in values.keys():
            print('hola')
        return super(ProductTemplate, self).write(values)
    

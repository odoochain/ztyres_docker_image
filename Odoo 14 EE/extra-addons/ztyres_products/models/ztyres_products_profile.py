from odoo import _, api, fields, models


class Profile(models.Model):
    _name = 'ztyres_products.profile'
    _description = 'New Description'
    _rec_name = 'number'

    number = fields.Float(string='Perfil', digits=(4, 2))
    

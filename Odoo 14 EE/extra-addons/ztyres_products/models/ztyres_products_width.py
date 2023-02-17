from odoo import _, api, fields, models


class Width(models.Model):
    _name = 'ztyres_products.width'
    _description = 'New Description'
    _rec_name = 'number'

    number = fields.Integer(string='Ancho')

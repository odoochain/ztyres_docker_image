# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class TireMeasure(models.Model):
    _name = "ztyres_products.tire_measure"
    _description = "Medida"

    width_id = fields.Many2one("ztyres_products.width", string="Ancho", ondelete="restrict")
    separator_id = fields.Many2one("ztyres_products.separator", string="Separador")
    profile_id = fields.Many2one("ztyres_products.profile", string="Perfil")
    rim_id = fields.Many2one("ztyres_products.rim", string="Rin")
    old_name = fields.Char(string="Medida antigua")
    name = fields.Char(compute="_compute_name", string="Medida")
    def _compute_name(self):
        for rec in self:
            if rec.width_id.number and rec.separator_id.character and rec.profile_id.number and rec.rim_id.number:
                rec.name = '%s%s%s%s%s'%(rec.width_id.number or '',rec.separator_id.character or '',rec.profile_id.number or '','R',rec.rim_id.number or '')
            else:
                rec.name = rec.old_name or 'N/A'

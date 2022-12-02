# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class ResCompany(models.Model): 
    _inherit = 'res.company'

    days_to_disolve = fields.Integer('Días para deshacer la reserva')

class ResConfigSettings(models.TransientModel): 
    _inherit = 'res.config.settings'


    days_to_disolve = fields.Integer('Días para deshacer la reserva', related='company_id.days_to_disolve', readonly=False)
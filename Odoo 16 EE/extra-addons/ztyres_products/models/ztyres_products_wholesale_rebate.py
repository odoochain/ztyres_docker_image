# -*- coding: utf-8 -*-
from odoo import _, api, fields, models

class WholesaleRebate(models.Model):
	_name = 'ztyres_products.wholesale_rebate'
	_description = 'Rebate de mayoreo'

	name = fields.Char(string='RM')

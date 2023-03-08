# -*- coding: utf-8 -*-
# from odoo import http


# class ZtyresSale(http.Controller):
#     @http.route('/ztyres_sale/ztyres_sale', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ztyres_sale/ztyres_sale/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ztyres_sale.listing', {
#             'root': '/ztyres_sale/ztyres_sale',
#             'objects': http.request.env['ztyres_sale.ztyres_sale'].search([]),
#         })

#     @http.route('/ztyres_sale/ztyres_sale/objects/<model("ztyres_sale.ztyres_sale"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ztyres_sale.object', {
#             'object': obj
#         })

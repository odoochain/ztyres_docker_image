# -*- coding: utf-8 -*-
# from odoo import http


# class SaleApprove(http.Controller):
#     @http.route('/sale_approve/sale_approve/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_approve/sale_approve/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_approve.listing', {
#             'root': '/sale_approve/sale_approve',
#             'objects': http.request.env['sale_approve.sale_approve'].search([]),
#         })

#     @http.route('/sale_approve/sale_approve/objects/<model("sale_approve.sale_approve"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_approve.object', {
#             'object': obj
#         })

# -*- coding: utf-8 -*-
# from odoo import http


# class HrExpenseExt(http.Controller):
#     @http.route('/hr_expense_ext/hr_expense_ext/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_expense_ext/hr_expense_ext/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_expense_ext.listing', {
#             'root': '/hr_expense_ext/hr_expense_ext',
#             'objects': http.request.env['hr_expense_ext.hr_expense_ext'].search([]),
#         })

#     @http.route('/hr_expense_ext/hr_expense_ext/objects/<model("hr_expense_ext.hr_expense_ext"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_expense_ext.object', {
#             'object': obj
#         })

# -*- coding: utf-8 -*-
# from odoo import http


# class EmpCode(http.Controller):
#     @http.route('/emp_code/emp_code', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/emp_code/emp_code/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('emp_code.listing', {
#             'root': '/emp_code/emp_code',
#             'objects': http.request.env['emp_code.emp_code'].search([]),
#         })

#     @http.route('/emp_code/emp_code/objects/<model("emp_code.emp_code"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('emp_code.object', {
#             'object': obj
#         })


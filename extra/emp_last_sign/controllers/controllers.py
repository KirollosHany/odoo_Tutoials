# -*- coding: utf-8 -*-
# from odoo import http


# class EstateManager(http.Controller):
#     @http.route('/emp_last_sign/emp_last_sign', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/emp_last_sign/emp_last_sign/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('emp_last_sign.listing', {
#             'root': '/emp_last_sign/emp_last_sign',
#             'objects': http.request.env['emp_last_sign.emp_last_sign'].search([]),
#         })

#     @http.route('/emp_last_sign/emp_last_sign/objects/<model("emp_last_sign.emp_last_sign"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('emp_last_sign.object', {
#             'object': obj
#         })


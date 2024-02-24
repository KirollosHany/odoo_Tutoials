# -*- coding: utf-8 -*-
# from odoo import http


# class CrmCus(http.Controller):
#     @http.route('/crm_cus/crm_cus', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_cus/crm_cus/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_cus.listing', {
#             'root': '/crm_cus/crm_cus',
#             'objects': http.request.env['crm_cus.crm_cus'].search([]),
#         })

#     @http.route('/crm_cus/crm_cus/objects/<model("crm_cus.crm_cus"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_cus.object', {
#             'object': obj
#         })


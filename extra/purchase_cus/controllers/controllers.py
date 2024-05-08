# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseCus(http.Controller):
#     @http.route('/purchase_cus/purchase_cus', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_cus/purchase_cus/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_cus.listing', {
#             'root': '/purchase_cus/purchase_cus',
#             'objects': http.request.env['purchase_cus.purchase_cus'].search([]),
#         })

#     @http.route('/purchase_cus/purchase_cus/objects/<model("purchase_cus.purchase_cus"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_cus.object', {
#             'object': obj
#         })


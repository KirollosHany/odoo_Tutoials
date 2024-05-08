# -*- coding: utf-8 -*-
# from odoo import http


# class Amofouad(http.Controller):
#     @http.route('/amofouad/amofouad', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/amofouad/amofouad/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('amofouad.listing', {
#             'root': '/amofouad/amofouad',
#             'objects': http.request.env['amofouad.amofouad'].search([]),
#         })

#     @http.route('/amofouad/amofouad/objects/<model("amofouad.amofouad"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('amofouad.object', {
#             'object': obj
#         })


# -*- coding: utf-8 -*-

from odoo import api, fields, models


class CrmLead(models.Model):
     _inherit = 'crm.lead'

     costing = fields.Char(string='cost of project')

# -*- coding: utf-8 -*-

from datetime import date
from odoo import api, fields, models


class emp_code(models.Model):
     _inherit = 'hr.employee'

     Employee_Code = fields.Char(string='Employee Code')
     Emp_start_date = fields.Date(string='Start Date')
     Emp_type = fields.Selection([('Portal', 'Portal User') , ('internal','Internal User')] , string='User Type')





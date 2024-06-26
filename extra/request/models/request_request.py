# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class request(models.Model):
    _name = 'request.request'
    _description = 'request.request'
    _inherit = ['mail.thread.cc',  'mail.activity.mixin']


    req_name = fields.Char(string="Request Name" ,tracking=True)
    name = fields.Many2one("res.users", string="Employee Name", default=lambda self: self.env.user, tracking=True , readonly=1 )

    request = fields.Selection([
        ('HR Letter' , 'HR Letter'),
        ('Expenses' , 'Expenses')
    ],
    string = "Request Type",
    required = True,
    copy = False,
    tracking = True,
    )
    reason = fields.Char(string="Reason")

    project = fields.Many2one('project.project', string='Project', required=True, tracking=True)

    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        required=True,
        copy=True,
    )

    approve_manager_id = fields.Many2one(
        'hr.employee',
        string='Department Manager',
        #readonly=True,
        copy=False,
        # related='employee_'
    )
    reject_manager_id = fields.Many2one(
        'hr.employee',
        string='Department Manager Reject',
        readonly=True,
    )
    #
    date = fields.Datetime(string="Date", default=fields.Datetime.now(), readonly=1)

    # manager_id = fields.Many2one('hr.employee', string='Direct Manager', compute='_compute_manager_id', store=True)
    #
    # @api.depends('employee_id')
    # def _compute_manager_id(self):
    #     for record in self:
    #         if record.employee_id:
    #             record.manager_id = record.employee_id.parent_id.id
    #         else:
    #             record.manager_id = False

# f_app_name = fields.Many2one("employee_parent_id", string="Employee Name", tracking=True )
   #  manager_id = fields.Many2one('hr.employee', string='Manager', tracking=True, check_company=True)



    # def _update_employee_manager(self, manager_id):
    #     employees = self.env['hr.employee']
    #     for department in self:
    #         employees = employees | self.env['hr.employee'].search([
    #             ('id', '!=', manager_id),
    #             ('department_id', '=', department.id),
    #             ('parent_id', '=', department.manager_id.id)
    #         ])
    #     employees.write({'parent_id': manager_id})







    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100


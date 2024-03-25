# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models

from odoo.addons.account.models.company import PEPPOL_LIST


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    manager_1 = fields.Many2one('res.users',string="first manager", config_parameter='estate.manager1')
    manager_2 = fields.Many2one('res.users',string="sec manager", config_parameter='estate.manager2')
    manager_3 = fields.Many2one('res.users',string="third manager", config_parameter='estate.manager3')
    manager_4 = fields.Many2one('res.users',string="forth manager", config_parameter='estate.manager4')
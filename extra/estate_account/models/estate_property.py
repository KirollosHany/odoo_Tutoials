# -*- coding: utf-8 -*-

from odoo import models, Command , fields


class EstateProperty(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "estate.property"

    invoiced_id = fields.Many2one('account.move')

    # ---------------------------------------- Action Methods -------------------------------------

    # def action_invoice(self):
    #     res = super().action_invoice()
    #     journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
    #     # Another way to get the journal:
    #     # journal = self.env["account.move"].with_context(default_move_type="out_invoice")._get_default_journal()
    #     for prop in self:
    #         invoiced = self.env["account.move"].create(
    #             {
    #                 "partner_id": prop.buyer_id.id,
    #                 "move_type": "out_invoice",
    #                 "journal_id": journal.id,
    #                 "invoice_line_ids": [
    #                     Command.create({
    #                         "name": prop.name,
    #                         "product_id": prop.property_type_id.product_id.id,
    #                         "quantity": 1.0,
    #                         "price_unit": prop.selling_price * 100.0 / 100.0,
    #                     }),
    #                     Command.create({
    #                         "name": "Administrative fees",
    #                         "product_id": 48.0,
    #                         "quantity": 1.0,
    #                         "price_unit": 100.0,
    #                     }),
    #                 ],
    #             }
    #         )
    #         self.invoiced.id = invoiced.id
    #     return res
# from odoo import api, fields, models, Command, _
#
#
# class RealEstateInstaWizard(models.TransientModel):
#     _name = 'estat.payment.wizard'
#     _description = 'Create Automatic Installment Invoices'
#
#     periods = fields.Selection(
#             [('1', 'immediate'),
#              ('6', '6 Months'),
#              ('12', '12 Months'),
#              ('24', '24 Months')],
#             default='6',
#             string='Installments Periods',
#     )
#
#
# def action_invoice_ins(self):
#     # res = super().action_invoice()
#     property_id = self.env.context.get('active_id')
#     props = self.env['estate.property'].browse(property_id)
#     journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
#     # Another way to get the journal:
#     # journal = self.env["account.move"].with_context(default_move_type="out_invoice")._get_default_journal()
#     for prop in props:
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

# -*- coding: utf-8 -*-
# Part of Odoo. Tutorials.

from odoo import api, fields, models, Command, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class RealEstateInstaWizard(models.TransientModel):
    _name = 'estat.payment.wizard'
    _description = 'Create Automatic Installment Invoices'

    fees_amount = fields.Float('Fees Amount', )
    periods = fields.Selection(
        [('1', 'immediate'),
         ('6', '6 Months'),
         ('12', '12 Months'),
         ('24', '24 Months')],
        default='6',
        string='Installments Periods',

    )

    def action_invoice_ins(self):
        property_id = self.env.context.get('active_id')
        props = self.env['estate.property'].browse(property_id)
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        # Another way to get the journal:
        # journal = self.env["account.move"].with_context(default_move_type="out_invoice")._get_default_journal()
        if self.periods:
            num_installments = int(self.periods)
            if not self.fees_amount or self.fees_amount <= 0:
                raise UserError("Fees amount must be specified and greater than zero.")

            for prop in props:
                total_price = prop.selling_price
                installment_price = total_price / num_installments

                for i in range(num_installments):
                    invoice_date_due = date.today() + relativedelta(months=i + 1)

                    invoice_vals = {
                        "partner_id": prop.buyer_id.id,
                        "move_type": "out_invoice",
                        "invoice_date_due": invoice_date_due,
                        "journal_id": journal.id,
                        "invoice_line_ids": [
                            Command.create({
                                "name": prop.name,
                                "product_id": prop.property_type_id.product_id.id,
                                "quantity": 1.0,
                                "price_unit": installment_price,
                            }),
                        ],
                    }

                    # Include fees amount only for the first installment
                    if i == 0:
                        invoice_vals["invoice_line_ids"].append(
                            Command.create({
                                "name": "Administrative fees",
                                "product_id": 48.0,
                                "quantity": 1.0,
                                "price_unit": self.fees_amount,
                            })
                        )

                    self.env["account.move"].create(invoice_vals)

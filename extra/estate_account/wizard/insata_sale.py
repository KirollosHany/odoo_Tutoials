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

                for i in range(0, num_installments):

                    invoice_vals = {
                        "partner_id": prop.buyer_id.id,
                        "move_type": "out_invoice",
                        "invoice_date_due": date.today() + relativedelta(months=i+1),
                        "journal_id": journal.id,
                        "invoice_line_ids": [
                            Command.create({
                                "name": prop.name,
                                "product_id": prop.property_type_id.product_id.id,
                                "quantity": 1.0,
                                "price_unit": (prop.selling_price/num_installments),
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
                    prop.write({'state': 'Invoicing'})
                    raise UserError("Invoices have been created for this property.")
                    return {
                        'type': 'ir.actions.act_window_close'}  # This line might be removed, depending on your requirement

                return {'type': 'ir.actions.act_window_close'}
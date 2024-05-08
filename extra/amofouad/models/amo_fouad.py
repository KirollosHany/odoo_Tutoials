from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError



class AmoFouad(models.Model):
    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "amo.fouad"
    _description = "Amo Fouad"
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _order = "id desc"


    name = fields.Char("Title", required=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("canceled", "Canceled"),
            ("sold", "Sold"),
            ("Invoicing", "Create Invoice"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
        tracking=True
    )

    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Canceled properties cannot be sold.")
        return self.write({"state": "sold"})

    def action_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError("Sold properties cannot be canceled.")
        return self.write({"state": "canceled"})

    def action_invoice(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Invoicing properties cannot be Created.")
        return self.write({"state": "Invoicing"})

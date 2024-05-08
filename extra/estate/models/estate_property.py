# -*- coding: utf-8 -*-


from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "estate.property"
    _description = "Real Estate Property"
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _order = "id desc"

    # ---------------------------------------- Default Methods ------------------------------------

    def _default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)

    # def manager_1(self):
    #     manager1 = self.env['ir.config_parameter'].sudo().get_param('estate.manager1')
    #     return int(manager1)
    #     tracking = True

    def manager_2(self):
        manager1 = self.env['ir.config_parameter'].sudo().get_param('estate.manager2')
        return int(manager1)


    def manager_3(self):
        manager1 = self.env['ir.config_parameter'].sudo().get_param('estate.manager3')
        return int(manager1)

    def manager_4(self):
        manager1 = self.env['ir.config_parameter'].sudo().get_param('estate.manager4')
        return int(manager1)

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", default=lambda self: self._default_date_availability(),
                                    copy=False)
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", copy=False, readonly=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("N", "North"),
            ("S", "South"),
            ("E", "East"),
            ("W", "West"),
        ],
        string="Garden Orientation",
    )

    #
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'), ('2', 'Hot')], default='1')

    #

    # Special
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("canceled", "Canceled"),
            ('approved1', 'First Approval'),
            ('approved2', 'Sec Approval'),
            ('approved3', 'Third Approval'),
            ('approved4', 'Forth Approval'),
            ('reject', 'Rejected'),
            ("sold", "Sold"),
            ("Invoicing", "Create Invoice"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
        tracking=True
    )
    active = fields.Boolean("Active", default=True)

    # Relational
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # Computed
    total_area = fields.Integer(
        "Total Area (sqm)",
        compute="_compute_total_area",
        help="Total area computed by summing the living area and the garden area",
    )
    best_price = fields.Float("Best Offer", compute="_compute_best_price", help="Best offer received")

    # ---------------------------------------- Compute methods ------------------------------------

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.offer_ids.mapped("price")) if prop.offer_ids else 0.0

    # ----------------------------------- Constrains and Onchanges --------------------------------

    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for prop in self:
            if (
                    not float_is_zero(prop.selling_price, precision_rounding=0.01)
                    and float_compare(prop.selling_price, prop.expected_price * 90.0 / 100.0,
                                      precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "N"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    manager_1 = fields.Many2one(
        'res.users',
        string="First Manager",
        help="Department manager assigned to this property",
        compute='_compute_manager_1',
        store=True
    )

    @api.depends('user_id')
    def _compute_manager_1(self):
        for record in self:
            if record.user_id and record.user_id.employee_ids:
                manager_employee = record.user_id.employee_ids[0].parent_id
                if manager_employee:
                    manager_user = manager_employee.user_id
                    if manager_user:
                        record.manager_1 = manager_user
            else:
                record.manager_1 = False

    def manager_approval_1(self):
        # Compute manager_1 if not set
        self._compute_manager_1()

        # Get the user who created the property
        created_user = self.user_id

        # Get the parent user of the current user
        current_user_parent = self.env.user

        # Check if the current user's parent matches the user who created the property
        if not created_user or current_user_parent != self.manager_1:
            raise UserError("Only the parent user of the creator can approve this property.")

        # Update the state to 'approved1'
        self.write({"state": "approved1"})

        return True



    # ------------------------------------------ CRUD Methods -------------------------------------

    # @api.ondelete(at_uninstall=False)
    # def _unlink_if_new_or_canceled(self):
    #     if not set(self.mapped("state")) <= {"new", "canceled"}:
    #         raise UserError("Only new and canceled properties can be deleted.")

    # ---------------------------------------- Action Methods -------------------------------------

    # def manager_approval_1(self):
    #     # # print(self.env.user.id)
    #     # # print(self.manager_1())
    #     # if self.env.user.id == self.manager_1():
    #     #     print('approve1')
    #     #     return self.write({"state": "approved1"})
    #     # else:
    #     #
    #     #     raise UserError("You Must be A Manager to do this .")
    #
    #     if not self.env.user.has_group('estate.employee_manager1'):
    #         raise UserError("Only Admin users can cancel properties.")
    #     return self.write({"state": "approved1"})

    def manager_approval_2(self):
        if self.env.user.id == self.manager_2():
            print('approve2')
            return self.write({"state": "approved2"})
        else:
            raise UserError("You Must be A Manager to do this .")
        # if not self.env.user.has_group('estate.employee_manager2'):
        #     raise UserError("Only Admin users can cancel properties.")
        # return self.write({"state": "approved2"})

    def manager_approval_3(self):
        if self.env.user.id == self.manager_3():
            print('approve3')
            return self.write({"state": "approved3"})
        else:
            raise UserError("You Must be A Manager to do this .")

    def manager_approval_4(self):
        if self.env.user.id == self.manager_4():
            print('approve4')
            return self.write({"state": "approved4"})
        else:
            raise UserError("You Must be A Manager to do this .")

    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Canceled properties cannot be sold.")
        return self.write({"state": "sold"})

    def action_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError("Sold properties cannot be canceled.")
        if not self.env.user.has_group('estate.employee_manager'):
            raise UserError("Only Admin users can cancel properties.")
        return self.write({"state": "canceled"})

    def action_invoice(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Invoicing properties cannot be Created.")
        return self.write({"state": "Invoicing"})

    ###



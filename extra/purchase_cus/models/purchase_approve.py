from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class PurchaseApprove(models.Model):
    _inherit = 'purchase.order'


def manager_2(self):
    manager1 = self.env['ir.config_parameter'].sudo().get_param('estate.manager2')
    return int(manager1)


def manager_3(self):
    manager1 = self.env['ir.config_parameter'].sudo().get_param('estate.manager3')
    return int(manager1)


def manager_4(self):
    manager1 = self.env['ir.config_parameter'].sudo().get_param('estate.manager4')
    return int(manager1)


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

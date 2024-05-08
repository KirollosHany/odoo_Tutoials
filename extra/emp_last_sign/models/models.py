from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    last_sign_in = fields.Datetime(string='Last Sign In', readonly=True)

class ResUsers(models.Model):
    _inherit = 'res.users'

    def _login(self, db, login, password, user_agent_env=None):
        uid = super(ResUsers, self)._login(db, login, password, user_agent_env=user_agent_env)
        if uid:
            employee = self.env['hr.employee'].search([('user_id', '=', uid)], limit=1)
            if employee:
                employee.write({'last_sign_in': fields.Datetime.now()})
        return uid

    @classmethod
    def authenticate(cls, db, login, password, user_agent_env=None):
        return cls._login(db, login, password, user_agent_env=user_agent_env)

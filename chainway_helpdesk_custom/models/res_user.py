from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    show_device_ui = fields.Boolean(
        string="Enable Device UI",
        help="Allow user to see Device UI / Views"
    )

    # @api.onchange('show_device_ui')
    # def _onchange_show_device_ui(self):
    #     group = self.env.ref('chainway_helpdesk_custom.group_device_user')
    #     if self.show_device_ui:
    #         self.groups_id |= group
    #     else:
    #         self.groups_id -= group
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

    #     for user in self:
    #         if user.show_device_ui:
    #             user.group_ids |= group
    #         else:
    #             user.group_ids -= group


    @api.onchange('show_device_ui')
    def _onchange_show_device_ui(self):
        group = self.env.ref('chainway_helpdesk_custom.group_device_user')

        for user in self:
            current_groups = user.group_ids.ids

            if user.show_device_ui:
                # add group
                if group.id not in current_groups:
                    user.group_ids = [(6, 0, current_groups + [group.id])]
            else:
                # remove group
                if group.id in current_groups:
                    new_groups = [gid for gid in current_groups if gid != group.id]
                    user.group_ids = [(6, 0, new_groups)]


    
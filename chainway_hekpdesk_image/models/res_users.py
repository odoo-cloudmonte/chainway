from odoo import models, fields, api
import random
import string
from odoo import api, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    mis_access = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string="MIS Access", default='no')

    def write(self, vals):
        res = super().write(vals)
        group = self.env.ref('chainway_helpdesk_custom.device_inventory_mis')

        for user in self:
            current_groups = user.group_ids.ids
            if user.mis_access == 'yes':
                if group.id not in current_groups:
                    user.group_ids = [(6, 0, current_groups + [group.id])]
                # user.groups_id = [(4, group.id)]
            else:
                # user.groups_id = [(3, group.id)].
                if group.id in current_groups:
                    new_groups = [gid for gid in current_groups if gid != group.id]
                    user.group_ids = [(6, 0, new_groups)]

        return res
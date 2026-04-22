from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    show_device_ui = fields.Boolean(
        string="Enable Device UI",
        help="Allow user to see Device UI / Views"
    )
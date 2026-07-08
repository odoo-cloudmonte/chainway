from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    show_import_button = fields.Boolean(
        string="Show Import Devices Button",
        config_parameter='chainway_helpdesk_custom.show_import_button'
    )
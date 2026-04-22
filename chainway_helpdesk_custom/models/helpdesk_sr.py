from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HelpdeskSr(models.Model):
    _name = "helpdesk.sr"

    device_sn = fields.Char(string="Device SN")
    description = fields.Char(string="Description")
    model_mo = fields.Char(string="Model No")

    ticket_id = fields.Many2one(
                'ticket.helpdesk',
                string="Tickets"
            )


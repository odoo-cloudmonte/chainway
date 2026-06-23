from collections import defaultdict

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HelpdeskSr(models.Model):
    _name = "helpdesk.sr"
    _rec_name ='device_sn'

    device_sn = fields.Char(string="Device SN")
    description = fields.Char(string="Description")
    model_mo = fields.Char(string="Model No")
    device_condition = fields.Selection([
        ('poor', 'Poor'),
        ('moderate', 'Moderate'),
        ('good','Good')
    ], string="Device Condition", tracking=True)
    remark = fields.Char(string="Remarks")
    

    ticket_id = fields.Many2one(
                'ticket.helpdesk',
                string="Tickets"
            )
    sequence = fields.Integer(string="S.No.", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        ticket_sequences = defaultdict(int)

        # Initialize with existing max sequence for each ticket
        for vals in vals_list:
            ticket_id = vals.get("ticket_id")
            if ticket_id and ticket_id not in ticket_sequences:
                last = self.search(
                    [("ticket_id", "=", ticket_id)],
                    order="sequence desc",
                    limit=1,
                )
                ticket_sequences[ticket_id] = last.sequence or 0

        # Assign sequence
        for vals in vals_list:
            ticket_id = vals.get("ticket_id")
            if ticket_id and not vals.get("sequence"):
                ticket_sequences[ticket_id] += 1
                vals["sequence"] = ticket_sequences[ticket_id]

        return super().create(vals_list)

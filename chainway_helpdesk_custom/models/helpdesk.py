from datetime import timedelta
import re

from odoo import api, models, fields
from odoo.exceptions import ValidationError

class TicketHelpdesk(models.Model):
    _inherit = 'ticket.helpdesk'

    # device_ids = fields.Many2many(
    #     'device.inventory',
    #     'ticket_device_rel',   # relation table name
    #     'ticket_id',           # column for this model
    #     'device_id',           # column for device model
    #     string="Devices"
    # )

    sr_ids = fields.One2many(
        'helpdesk.sr',   # target model
        'ticket_id',     # inverse field
        string="Service Requests"
    )

    company_name = fields.Char(string="Company Name")
    company_address = fields.Char(string="Company Address")
    contact = fields.Char(string="Contact")
    store = fields.Char(string="Pin Code")

    is_overdue = fields.Boolean(compute="_compute_states", store=True)
    is_closed = fields.Boolean(compute="_compute_states", store=True)
    is_on_time = fields.Boolean(compute="_compute_states", store=True)
    # device_condition = fields.Selection([
    #     ('poor', 'Poor'),
    #     ('moderate', 'Moderate'),
    #     ('good','Good')
    # ], string="Device Condition", tracking=True)

    @api.depends('create_date', 'stage_id')
    def _compute_states(self):
        now = fields.Datetime.now()
        for rec in self:
            rec.is_overdue = False
            rec.is_closed = False
            rec.is_on_time = False

            if not rec.create_date:
                continue

            is_closed = rec.stage_id.closing_stage if rec.stage_id else False

            if is_closed:
                rec.is_closed = True
            elif now > rec.create_date + timedelta(hours=48):
                rec.is_overdue = True
            else:
                rec.is_on_time = True

    def cron_update_ticket_states(self):
        now = fields.Datetime.now()

        # tickets = self.search([])
        tickets = self.search([
            ('stage_id.closing_stage', '=', False)
        ])

        for rec in tickets:
            # Reset all states
            rec.is_overdue = False
            rec.is_closed = False
            rec.is_on_time = False

            if not rec.create_date:
                continue

            is_closed = rec.stage_id.closing_stage if rec.stage_id else False

            # 🟢 CLOSED
            if is_closed:
                rec.is_closed = True

            # 🔴 OVERDUE
            elif now > rec.create_date + timedelta(hours=48):
                rec.is_overdue = True

            # 🟡 ON TIME
            else:
                rec.is_on_time = True


    @api.constrains('create_date', 'start_date', 'end_date')
    def _check_ticket_dates(self):
        for rec in self:

            # create_date <= start_date
            if rec.create_date and rec.start_date:
                if rec.start_date < rec.create_date:
                    raise ValidationError(
                        "Start Date cannot be earlier than Creation Date."
                    )

            # start_date <= end_date
            if rec.start_date and rec.end_date:
                if rec.end_date < rec.start_date:
                    raise ValidationError(
                        "End Date cannot be earlier than Start Date."
                    )

            # create_date <= end_date
            if rec.create_date and rec.end_date:
                if rec.end_date < rec.create_date:
                    raise ValidationError(
                        "End Date cannot be earlier than Creation Date."
                    )
                
    @api.constrains('phone')
    def _check_phone_number(self):
        for rec in self:
            if rec.phone:
                phone = rec.phone.strip()

                # Allow only digits, optional + at start, length 10–15
                if not re.match(r'^\+?\d{10,15}$', phone):
                    raise ValidationError(
                        "Phone number must be 10–15 digits and can optionally start with '+'."
                    )
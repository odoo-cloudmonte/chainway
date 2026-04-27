from datetime import timedelta

from odoo import api, models, fields

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
    store = fields.Char(string="Store Location")

    is_overdue = fields.Boolean(compute="_compute_states", store=True)
    is_closed = fields.Boolean(compute="_compute_states", store=True)
    is_on_time = fields.Boolean(compute="_compute_states", store=True)

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
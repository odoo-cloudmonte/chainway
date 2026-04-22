from odoo import models, fields

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

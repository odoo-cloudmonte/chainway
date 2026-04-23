import base64
import io

import xlsxwriter

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DeviceInventory(models.Model):
    _name = 'device.inventory'
    _description = 'Device Inventory'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    

    device_sn = fields.Char(string="Device SN")
    accessories_sn = fields.Char(string="Accessories SN")
    type = fields.Selection([
        ('device', 'Device'),
        ('accessory', 'Accessory')
    ], string="Type")

    bt_mac = fields.Char(string="BT MAC")
    imei1 = fields.Char(string="IMEI 1")
    imei2 = fields.Char(string="IMEI 2")
    wifi_mac = fields.Char(string="WiFi MAC")
    model = fields.Char(string="Model")
    description = fields.Text(string="Descriptions")

    sw_version = fields.Char(string="SW Version")

    configuration_in = fields.Text(string="Configuration IN")
    configuration_out = fields.Text(string="Configuration OUT")

    warranty_wef = fields.Date(string="Warranty Effective From (WEF/DoP)")
    warranty_category = fields.Selection([
        ('standard', 'Standard'),
        ('extended', 'Extended'),
        ('none', 'None')
    ], string="Category Of Warranty")

    warranty_upto = fields.Date(string="Warranty Applicable Up To")

    # end_user_name = fields.Char(string="User Name")
    end_user_name = fields.Many2one(
        'res.partner',
        string="End User",
        tracking=True
    )

    po_date = fields.Date(string="PO Date")
    po_no = fields.Char(string="PO No")

    invoice_no = fields.Char(string="Invoice No")
    invoice_date = fields.Date(string="Invoice Date")

    location = fields.Char(string="Location")
    location_code = fields.Char(string="Location Code")

    shipping_address_po = fields.Text(string="Shipping Address (PO)")
    shipping_address_invoice = fields.Text(string="Shipping Address (Invoice)")
    delivery_location = fields.Char(string="Confirm Delivery Location")

    courier_name = fields.Char(string="Courier Name")
    tracking_id = fields.Char(string="Tracking ID")

    delivery_date = fields.Date(string="Delivery Date")

    pod_copy = fields.Binary(string="POD Copy", attachment=True)

    chainway_reference = fields.Char(string="Chainway CI Reference / Tax Invoice No")

    remark = fields.Text(string="Remark")

    name = fields.Char(string="Reference", compute="_compute_name", store=True)
    # ticket_id = fields.Many2one(
    #             'ticket.helpdesk',
    #             string="Tickets"
    #         )

    def _compute_name(self):
        for rec in self:
            rec.name = rec.device_sn or rec.imei1 or rec.end_user_name or "New"

    _sql_constraints = [
            ('device_sn_unique', 'unique(lower(device_sn))', 'Device SN must be unique!')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            device_sn = vals.get('device_sn')
            if device_sn:
                existing = self.search([
                    ('device_sn', '=ilike', device_sn)
                ], limit=1)
                if existing:
                    raise ValidationError("Device SN must be unique!")

        return super().create(vals_list)
    
    # def action_export_devices(self):
    #     output = io.BytesIO()
    #     workbook = xlsxwriter.Workbook(output)
    #     sheet = workbook.add_worksheet('Devices')

    #     headers = [
    #         "Device SN", "IMEI1", "Model",
    #         "End User", "PO No", "Invoice No",
    #         "Delivery Date", "POD Image"
    #     ]

    #     for col, header in enumerate(headers):
    #         sheet.write(0, col, header)

    #     row = 1

    #     for rec in self:
    #         sheet.write(row, 0, rec.device_sn or '')
    #         sheet.write(row, 1, rec.imei1 or '')
    #         sheet.write(row, 2, rec.model or '')
    #         sheet.write(row, 3, rec.end_user_name.name if rec.end_user_name else '')
    #         sheet.write(row, 4, rec.po_no or '')
    #         sheet.write(row, 5, rec.invoice_no or '')
    #         sheet.write(row, 6, str(rec.delivery_date or ''))

    #         # ✅ Insert image
    #         if rec.pod_copy:
    #             image_data = base64.b64decode(rec.pod_copy)
    #             image_stream = io.BytesIO(image_data)

    #             sheet.insert_image(row, 7, "pod.png", {
    #                 'image_data': image_stream,
    #                 'x_scale': 0.4,
    #                 'y_scale': 0.4
    #             })

    #         row += 1

    #     workbook.close()
    #     output.seek(0)

    #     file_data = base64.b64encode(output.read())

    #     attachment = self.env['ir.attachment'].create({
    #         'name': 'Device_Export.xlsx',
    #         'type': 'binary',
    #         'datas': file_data,
    #         'res_model': 'device.inventory',
    #     })

    #     return {
    #         'type': 'ir.actions.act_url',
    #         'url': f'/web/content/{attachment.id}?download=true',
    #         'target': 'self',
    #     }

    def action_open_import_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Import Devices',
            'res_model': 'device.import.wizard',
            'view_mode': 'form',
            'target': 'new',
        }


    def action_export_devices(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Devices')

        # ✅ ALL HEADERS
        headers = [
            "Device SN", "Accessories SN", "Type",
            "BT MAC", "IMEI1", "IMEI2", "WiFi MAC",
            "Model", "Description", "SW Version",
            "Configuration IN", "Configuration OUT",
            "Warranty WEF", "Warranty Category", "Warranty Upto",
            "End User",
            "PO Date", "PO No",
            "Invoice No", "Invoice Date",
            "Location", "Location Code",
            "Shipping Address PO", "Shipping Address Invoice",
            "Delivery Location",
            "Courier Name", "Tracking ID",
            "Delivery Date",
            "Chainway Reference",
            "Remark",
            "POD Image"
        ]

        # Write header
        for col, header in enumerate(headers):
            sheet.write(0, col, header)

        row = 1

        for rec in self:
            col = 0

            # ✅ Write all fields safely
            sheet.write(row, col, rec.device_sn or ''); col += 1
            sheet.write(row, col, rec.accessories_sn or ''); col += 1
            sheet.write(row, col, rec.type or ''); col += 1
            sheet.write(row, col, rec.bt_mac or ''); col += 1
            sheet.write(row, col, rec.imei1 or ''); col += 1
            sheet.write(row, col, rec.imei2 or ''); col += 1
            sheet.write(row, col, rec.wifi_mac or ''); col += 1
            sheet.write(row, col, rec.model or ''); col += 1
            sheet.write(row, col, rec.description or ''); col += 1
            sheet.write(row, col, rec.sw_version or ''); col += 1
            sheet.write(row, col, rec.configuration_in or ''); col += 1
            sheet.write(row, col, rec.configuration_out or ''); col += 1
            sheet.write(row, col, str(rec.warranty_wef or '')); col += 1
            sheet.write(row, col, rec.warranty_category or ''); col += 1
            sheet.write(row, col, str(rec.warranty_upto or '')); col += 1
            sheet.write(row, col, rec.end_user_name.name if rec.end_user_name else ''); col += 1
            sheet.write(row, col, str(rec.po_date or '')); col += 1
            sheet.write(row, col, rec.po_no or ''); col += 1
            sheet.write(row, col, rec.invoice_no or ''); col += 1
            sheet.write(row, col, str(rec.invoice_date or '')); col += 1
            sheet.write(row, col, rec.location or ''); col += 1
            sheet.write(row, col, rec.location_code or ''); col += 1
            sheet.write(row, col, rec.shipping_address_po or ''); col += 1
            sheet.write(row, col, rec.shipping_address_invoice or ''); col += 1
            sheet.write(row, col, rec.delivery_location or ''); col += 1
            sheet.write(row, col, rec.courier_name or ''); col += 1
            sheet.write(row, col, rec.tracking_id or ''); col += 1
            sheet.write(row, col, str(rec.delivery_date or '')); col += 1
            sheet.write(row, col, rec.chainway_reference or ''); col += 1
            sheet.write(row, col, rec.remark or ''); col += 1

            # ✅ Image (POD)
            if rec.pod_copy:
                try:
                    image_data = base64.b64decode(rec.pod_copy)
                    image_stream = io.BytesIO(image_data)

                    sheet.insert_image(row, col, "pod.png", {
                        'image_data': image_stream,
                        'x_scale': 0.4,
                        'y_scale': 0.4,
                    })
                except Exception:
                    sheet.write(row, col, "Invalid Image")
            else:
                sheet.write(row, col, '')

            row += 1

        # Optional: set column width
        sheet.set_column(0, len(headers), 20)

        workbook.close()
        output.seek(0)

        file_data = base64.b64encode(output.read())

        attachment = self.env['ir.attachment'].create({
            'name': 'Device_Export.xlsx',
            'type': 'binary',
            'datas': file_data,
            'res_model': 'device.inventory',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
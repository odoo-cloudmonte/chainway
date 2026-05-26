import base64
import io

import xlsxwriter
from PIL import Image

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DeviceInventory(models.Model):
    _name = 'device.inventory'
    _description = 'Device Inventory'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name ='device_sn'

    

    device_sn = fields.Char(string="Device SN", tracking=True)
    accessories_sn = fields.Char(string="Accessories SN", tracking=True)
    type = fields.Selection([
        ('device', 'Device'),
        ('accessory', 'Accessory'),
        ('accessories','Accessories')
    ], string="Type", tracking=True)

    bt_mac = fields.Char(string="BT MAC", tracking=True)
    imei1 = fields.Char(string="IMEI 1", tracking=True)
    imei2 = fields.Char(string="IMEI 2", tracking=True)
    wifi_mac = fields.Char(string="WiFi MAC", tracking=True)
    model = fields.Char(string="Model", tracking=True)
    description = fields.Text(string="Descriptions", tracking=True)

    sw_version = fields.Char(string="SW Version", tracking=True)

    configuration_in = fields.Text(string="Configuration IN", tracking=True)
    configuration_out = fields.Text(string="Configuration OUT", tracking=True)

    warranty_wef = fields.Date(string="Warranty Effective From (WEF/DoP)", tracking=True)
    warranty_category = fields.Selection([
        ('standard', 'Standard'),
        ('extended', 'Extended'),
        ('comprehensive','Comprehensive Warranty'),
        ('none', 'None')
    ], string="Category Of Warranty", tracking=True)

    warranty_upto = fields.Date(string="Warranty Applicable Up To", tracking=True)
    device_condition = fields.Selection([
        ('poor', 'Poor'),
        ('moderate', 'Moderate'),
        ('good','Good')
    ], string="Device Condition", tracking=True)

    # end_user_name = fields.Char(string="User Name")
    end_user_name = fields.Many2one(
        'res.partner',
        string="End User",
        tracking=True
    )

    po_date = fields.Date(string="PO Date", tracking=True)
    po_no = fields.Char(string="PO No", tracking=True)

    invoice_no = fields.Char(string="Invoice No", tracking=True)
    invoice_date = fields.Date(string="Invoice Date", tracking=True)

    location = fields.Char(string="Location", tracking=True)
    location_code = fields.Char(string="Location Code", tracking=True)

    shipping_address_po = fields.Text(string="Shipping Address (PO)", tracking=True)
    shipping_address_invoice = fields.Text(string="Shipping Address (Invoice)", tracking=True)
    delivery_location = fields.Char(string="Confirm Delivery Location", tracking=True)

    courier_name = fields.Char(string="Courier Name", tracking=True)
    tracking_id = fields.Char(string="Tracking ID", tracking=True)

    delivery_date = fields.Date(string="Delivery Date", tracking=True)

    pod_copy = fields.Binary(string="POD Copy", attachment=True)
    pod_url = fields.Char(string="Pod URL")

    chainway_reference = fields.Char(string=" Chainway Tax Invoice No", tracking=True)

    Chainway_pi_no = fields.Char(string="Chainway PI No", tracking = True)

    remark = fields.Text(string="Remark", tracking=True)

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
    
    def action_download_template(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/chainway_helpdesk_custom/static/files/import_template.xlsx',
            'target': 'self',
        }
    

    @api.constrains(
        'warranty_wef',
        'warranty_upto',
        'po_date',
        'invoice_date',
        'delivery_date'
    )
    def _check_date_validations(self):
        for rec in self:

            # 1. Warranty validation
            if rec.warranty_wef and rec.warranty_upto:
                if rec.warranty_upto < rec.warranty_wef:
                    raise ValidationError(
                        "Warranty 'Applicable Up To' date cannot be before Warranty Start Date."
                    )

            # 2. Invoice date should not be before PO date
            if rec.po_date and rec.invoice_date:
                if rec.invoice_date < rec.po_date:
                    raise ValidationError(
                        "Invoice Date cannot be earlier than PO Date."
                    )

            # 3. Delivery date should not be before invoice date
            if rec.invoice_date and rec.delivery_date:
                if rec.delivery_date < rec.invoice_date:
                    raise ValidationError(
                        "Delivery Date cannot be earlier than Invoice Date."
                    )

            # 4. Delivery date should not be before PO date (optional but useful)
            if rec.po_date and rec.delivery_date:
                if rec.delivery_date < rec.po_date:
                    raise ValidationError(
                        "Delivery Date cannot be earlier than PO Date."
                    )
    
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
            "Device SN", "Type",
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
            "Chainway Tax Invoice No",
            "Chainway PI No",
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
            # sheet.write(row, col, rec.accessories_sn or ''); col += 1
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
            sheet.write(row,col, rec.pod_url or ''); col += 1

            # ✅ Image (POD)
            # if rec.pod_copy:
            #     try:
            #         image_data = base64.b64decode(rec.pod_copy)
            #         image_stream = io.BytesIO(image_data)

            #         sheet.insert_image(row, col, "pod.png", {
            #             'image_data': image_stream,
            #             'x_scale': 0.4,
            #             'y_scale': 0.4,
            #         })
            #     except Exception:
            #         sheet.write(row, col, "Invalid Image")
            # else:
            #     sheet.write(row, col, '')

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

    # def action_export_devices(self):

    #     output = io.BytesIO()

    #     workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    #     sheet = workbook.add_worksheet('Devices')

    #     # =========================
    #     # Formats
    #     # =========================
    #     header_format = workbook.add_format({
    #         'bold': True,
    #         'bg_color': '#D9E1F2',
    #         'border': 1,
    #         'align': 'center',
    #         'valign': 'vcenter'
    #     })

    #     text_format = workbook.add_format({
    #         'border': 1,
    #         'valign': 'top'
    #     })

    #     # =========================
    #     # Headers
    #     # =========================
    #     headers = [
    #         "Device SN", "Type",
    #         "BT MAC", "IMEI1", "IMEI2", "WiFi MAC",
    #         "Model", "Description", "SW Version",
    #         "Configuration IN", "Configuration OUT",
    #         "Warranty WEF", "Warranty Category", "Warranty Upto",
    #         "End User",
    #         "PO Date", "PO No",
    #         "Invoice No", "Invoice Date",
    #         "Location", "Location Code",
    #         "Shipping Address PO", "Shipping Address Invoice",
    #         "Delivery Location",
    #         "Courier Name", "Tracking ID",
    #         "Delivery Date",
    #         "Chainway Reference",
    #         "Remark",
    #         "POD Image"
    #     ]

    #     # Write Header
    #     for col, header in enumerate(headers):
    #         sheet.write(0, col, header, header_format)

    #     # Freeze Header Row
    #     sheet.freeze_panes(1, 0)

    #     # Default column width
    #     sheet.set_column(0, len(headers) - 2, 20)

    #     # POD Image column width
    #     image_col = len(headers) - 1
    #     sheet.set_column(image_col, image_col, 35)

    #     row = 1

    #     for rec in self:

    #         col = 0

    #         # =========================
    #         # Text Data
    #         # =========================
    #         values = [
    #             rec.device_sn or '',
    #             rec.type or '',
    #             rec.bt_mac or '',
    #             rec.imei1 or '',
    #             rec.imei2 or '',
    #             rec.wifi_mac or '',
    #             rec.model or '',
    #             rec.description or '',
    #             rec.sw_version or '',
    #             rec.configuration_in or '',
    #             rec.configuration_out or '',
    #             str(rec.warranty_wef or ''),
    #             rec.warranty_category or '',
    #             str(rec.warranty_upto or ''),
    #             rec.end_user_name.name if rec.end_user_name else '',
    #             str(rec.po_date or ''),
    #             rec.po_no or '',
    #             rec.invoice_no or '',
    #             str(rec.invoice_date or ''),
    #             rec.location or '',
    #             rec.location_code or '',
    #             rec.shipping_address_po or '',
    #             rec.shipping_address_invoice or '',
    #             rec.delivery_location or '',
    #             rec.courier_name or '',
    #             rec.tracking_id or '',
    #             str(rec.delivery_date or ''),
    #             rec.chainway_reference or '',
    #             rec.remark or '',
    #         ]

    #         for value in values:
    #             sheet.write(row, col, value, text_format)
    #             col += 1

    #         # =========================
    #         # POD Image
    #         # =========================
    #         if rec.pod_copy:
    #             try:
    #                 image_data = base64.b64decode(rec.pod_copy)

    #                 image_stream = io.BytesIO(image_data)

    #                 # Read image dimensions
    #                 img = Image.open(image_stream)
    #                 width, height = img.size

    #                 # Reset stream
    #                 image_stream.seek(0)

    #                 # Scale image
    #                 x_scale = 0.5
    #                 y_scale = 0.5

    #                 scaled_width = width * x_scale
    #                 scaled_height = height * y_scale

    #                 # Adjust row height dynamically
    #                 row_height = max(80, scaled_height)

    #                 # Adjust column width dynamically
    #                 column_width = max(35, scaled_width / 7)

    #                 sheet.set_row(row, row_height)
    #                 sheet.set_column(col, col, column_width)

    #                 # Insert image
    #                 sheet.insert_image(row, col, "pod.png", {
    #                     'image_data': image_stream,
    #                     'x_scale': x_scale,
    #                     'y_scale': y_scale,
    #                     'x_offset': 5,
    #                     'y_offset': 5,
    #                     'object_position': 1,
    #                 })

    #             except Exception:
    #                 sheet.write(row, col, "Invalid Image", text_format)

    #         else:
    #             sheet.write(row, col, '', text_format)

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
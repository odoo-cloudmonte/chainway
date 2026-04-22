from odoo import models, fields
import base64
import io
import openpyxl
import requests

# class DeviceImportWizard(models.TransientModel):
#     _name = 'device.import.wizard'
#     _description = 'Import Devices'

#     file = fields.Binary(string="Upload Excel", required=True)
#     file_name = fields.Char()

#     def action_import(self):
#         wb = openpyxl.load_workbook(io.BytesIO(base64.b64decode(self.file)))
#         sheet = wb.active

#         for row in sheet.iter_rows(min_row=2, values_only=True):
#             try:
#                 # 👇 Map fields (same order as export)
#                 device_sn = row[0]
#                 accessories_sn = row[1]
#                 type_val = row[2]
#                 bt_mac = row[3]
#                 imei1 = row[4]
#                 imei2 = row[5]
#                 wifi_mac = row[6]
#                 model = row[7]
#                 description = row[8]
#                 sw_version = row[9]
#                 config_in = row[10]
#                 config_out = row[11]
#                 warranty_wef = row[12]
#                 warranty_category = row[13]
#                 warranty_upto = row[14]
#                 end_user_name = row[15]
#                 po_date = row[16]
#                 po_no = row[17]
#                 invoice_no = row[18]
#                 invoice_date = row[19]
#                 location = row[20]
#                 location_code = row[21]
#                 shipping_po = row[22]
#                 shipping_invoice = row[23]
#                 delivery_location = row[24]
#                 courier_name = row[25]
#                 tracking_id = row[26]
#                 delivery_date = row[27]
#                 chainway_reference = row[28]
#                 remark = row[29]
#                 image_data = row[30]   # base64 or URL

#                 # 🔍 Handle Many2one (partner)
#                 partner = False
#                 if end_user_name:
#                     partner = self.env['res.partner'].search(
#                         [('name', '=', end_user_name)], limit=1
#                     )
#                     if not partner:
#                         partner = self.env['res.partner'].create({
#                             'name': end_user_name
#                         })

#                 # 🖼 Handle Image
#                 pod_copy = False

#                 if image_data:
#                     if isinstance(image_data, str) and image_data.startswith('http'):
#                         # URL case
#                         response = requests.get(image_data)
#                         if response.status_code == 200:
#                             pod_copy = base64.b64encode(response.content)
#                     else:
#                         # Base64 case
#                         try:
#                             pod_copy = base64.b64decode(image_data)
#                             pod_copy = base64.b64encode(pod_copy)
#                         except Exception:
#                             pod_copy = False

#                 # ✅ Create record
#                 self.env['device.inventory'].create({
#                     'device_sn': device_sn,
#                     'accessories_sn': accessories_sn,
#                     'type': type_val,
#                     'bt_mac': bt_mac,
#                     'imei1': imei1,
#                     'imei2': imei2,
#                     'wifi_mac': wifi_mac,
#                     'model': model,
#                     'description': description,
#                     'sw_version': sw_version,
#                     'configuration_in': config_in,
#                     'configuration_out': config_out,
#                     'warranty_wef': warranty_wef,
#                     'warranty_category': warranty_category,
#                     'warranty_upto': warranty_upto,
#                     'end_user_name': partner.id if partner else False,
#                     'po_date': po_date,
#                     'po_no': po_no,
#                     'invoice_no': invoice_no,
#                     'invoice_date': invoice_date,
#                     'location': location,
#                     'location_code': location_code,
#                     'shipping_address_po': shipping_po,
#                     'shipping_address_invoice': shipping_invoice,
#                     'delivery_location': delivery_location,
#                     'courier_name': courier_name,
#                     'tracking_id': tracking_id,
#                     'delivery_date': delivery_date,
#                     'chainway_reference': chainway_reference,
#                     'remark': remark,
#                     'pod_copy': pod_copy,
#                 })

#             except Exception as e:
#                 raise Exception(f"Error on row {row}: {str(e)}")

import base64
import io
import openpyxl
import requests
from odoo import models, fields
from datetime import datetime

class DeviceImportWizard(models.TransientModel):
    _name = 'device.import.wizard'
    _description = 'Import Devices'

    file = fields.Binary(string="Upload Excel", required=True)
    file_name = fields.Char()

    def _parse_date(self, value):
        """Convert Excel date safely"""
        if not value:
            return False
        if isinstance(value, datetime):
            return value.date()
        return value  # already string or valid

    def action_import(self):
        wb = openpyxl.load_workbook(io.BytesIO(base64.b64decode(self.file)))
        sheet = wb.active

        headers = [cell.value for cell in sheet[1]]

        for index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            row_dict = dict(zip(headers, row))

            image_data = row_dict.get('POD Image')

        # for index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):

            try:
                # 🚫 Skip completely empty row
                if not any(row):
                    continue

                device_sn = row[0]

                # 🚫 Skip if no device_sn (optional rule)
                if not device_sn:
                    continue

                # 🔁 Prevent duplicate crash
                existing = self.env['device.inventory'].search([
                    ('device_sn', '=ilike', device_sn)
                ], limit=1)
                if existing:
                    continue  # skip instead of crash

                # 🔍 Partner handling
                partner = False
                if row[15]:
                    partner = self.env['res.partner'].search(
                        [('name', '=', row[15])], limit=1
                    )
                    if not partner:
                        partner = self.env['res.partner'].create({
                            'name': row[15]
                        })

                # 🖼 Image handling
                pod_copy = False
                # image_data = row[30]

                if image_data:
                    if isinstance(image_data, str) and image_data.startswith('http'):
                        try:
                            response = requests.get(image_data, timeout=5)
                            if response.status_code == 200:
                                pod_copy = base64.b64encode(response.content)
                        except Exception:
                            pod_copy = False
                    else:
                        try:    
                            pod_copy = image_data if isinstance(image_data, bytes) else base64.b64decode(image_data)
                        except Exception:
                            pod_copy = False

                # ✅ Create record
                self.env['device.inventory'].create({
                    'device_sn': device_sn,
                    'accessories_sn': row[1],
                    'type': row[2],
                    'bt_mac': row[3],
                    'imei1': row[4],
                    'imei2': row[5],
                    'wifi_mac': row[6],
                    'model': row[7],
                    'description': row[8],
                    'sw_version': row[9],
                    'configuration_in': row[10],
                    'configuration_out': row[11],
                    'warranty_wef': self._parse_date(row[12]),
                    'warranty_category': row[13],
                    'warranty_upto': self._parse_date(row[14]),
                    'end_user_name': partner.id if partner else False,
                    'po_date': self._parse_date(row[16]),
                    'po_no': row[17],
                    'invoice_no': row[18],
                    'invoice_date': self._parse_date(row[19]),
                    'location': row[20],
                    'location_code': row[21],
                    'shipping_address_po': row[22],
                    'shipping_address_invoice': row[23],
                    'delivery_location': row[24],
                    'courier_name': row[25],
                    'tracking_id': row[26],
                    'delivery_date': self._parse_date(row[27]),
                    'chainway_reference': row[28],
                    'remark': row[29],
                    'pod_copy': pod_copy,
                })

            except Exception as e:
                raise Exception(f"Error on Excel row {index}: {str(e)}")
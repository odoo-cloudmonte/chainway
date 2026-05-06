# -*- coding: utf-8 -*-
from odoo import models, fields, api
import uuid
from werkzeug.urls import url_quote

class ImageRecord(models.Model):
    _name = 'image.record'
    _description = 'Image Record'

    # name = fields.Char(string="Name", required=True)
    name = fields.Char(string="Reference", required=True, copy=False, readonly=True, default='New')
    image = fields.Binary(string="Image", attachment=True)
    image_url = fields.Char(string="Image URL", compute="_compute_image_url", store=True)
    access_token = fields.Char(string="Access Token", readonly=True)

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         vals['access_token'] = str(uuid.uuid4())
    #     return super().create(vals_list)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Sequence generation
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('image.record.seq') or 'New'

            # Token generation
            if not vals.get('access_token'):
                vals['access_token'] = str(uuid.uuid4())

        return super().create(vals_list)

    # @api.depends('access_token')
    # def _compute_image_url(self):
    #     base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #     for record in self:
    #         if record.access_token:
    #             record.image_url = f"{base_url}/image_link/{record.access_token}"
    #         else:
    #             record.image_url = False


    @api.depends('access_token', 'name')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for record in self:
            if record.access_token and record.name:
                safe_name = url_quote(record.name)
                record.image_url = f"{base_url}/image_link/{record.access_token}/{safe_name}"
            else:
                record.image_url = False
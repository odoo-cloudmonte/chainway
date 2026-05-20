# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64

class ImageController(http.Controller):

    # @http.route('/image_link/<string:token>', type='http', auth='public')
    # def get_image(self, token, **kwargs):
    #     record = request.env['image.record'].sudo().search([('access_token', '=', token)], limit=1)

    #     if not record or not record.image:
    #         return request.not_found()

    #     image_data = base64.b64decode(record.image)

    #     return request.make_response(
    #         image_data,
    #         headers=[
    #             ('Content-Type', 'image/png'),
    #             ('Content-Length', len(image_data))
    #         ]
    #     )

    # @http.route('/image_link/<string:token>/<string:name>', type='http', auth='public')
    # def get_image(self, token, name=None, **kwargs):
    #     record = request.env['image.record'].sudo().search(
    #         [('access_token', '=', token)], limit=1
    #     )

    #     if not record or not record.image:
    #         return request.not_found()

    #     image_data = base64.b64decode(record.image)

    #     return request.make_response(
    #         image_data,
    #         headers=[
    #             ('Content-Type', 'image/png'),
    #             ('Content-Length', len(image_data))
    #         ]
    #     )

    @http.route('/image/<string:name>', type='http', auth='public', website=True)
    def get_image(self, name=None, **kwargs):

        record = request.env['image.record'].sudo().search(
            [('name', '=', name)],
            limit=1
        )

        if not record or not record.image:
            return request.not_found()

        image_data = base64.b64decode(record.image)

        return request.make_response(
            image_data,
            headers=[
                ('Content-Type', 'image/png'),
                ('Content-Length', str(len(image_data)))
            ]
        )
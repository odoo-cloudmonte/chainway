import base64

from odoo import http
from odoo.http import request
from datetime import date

class WarrantyController(http.Controller):

    @http.route(['/warranty-check'], type='http', auth='public', website=True)
    def warranty_form(self, **kwargs):
        return request.render('chainway_helpdesk_custom.warranty_form_template')

    @http.route(['/warranty-result'], type='http', auth='public', website=True, methods=['POST'])
    def warranty_result(self, **post):
        search_sn = post.get('search_sn')

        device = request.env['device.inventory'].sudo().search([
            '|', '|',
            ('device_sn', '=', search_sn),
            ('imei1', '=', search_sn),
            ('imei2', '=', search_sn),
        ], limit=1)

        result = {}
        if device:
            if device.warranty_upto:
                status = "In Warranty" if device.warranty_upto >= date.today() else "Expired"
            else:
                status = "No Warranty Info"

            result = {
                'found': True,
                'device': device,
                'status': status,
            }
        else:
            result = {
                'found': False,
                'status': "Device Not Found"
            }

        return request.render('chainway_helpdesk_custom.warranty_result_template', result)

    @http.route('/smart/form', type='http', auth='public', website=True)
    def smart_form(self, **kw):

        return request.render(
            'chainway_helpdesk_custom.smart_form_template',
            {
                'data': kw
            }
        )

    @http.route('/my/helpdesk/form', type='http', auth='user', website=True)
    def helpdesk_form(self, **kw):

        return request.render('chainway_helpdesk_custom.portal_helpdesk_form', {
            'page_name': 'helpdesk_form'
        })
    
    @http.route('/my/helpdesk/submit', type='http', auth='public', website=True, csrf=True)
    def submit_ticket(self, **post):

        

        models = request.httprequest.form.getlist('model_number[]')
        serials = request.httprequest.form.getlist('serial_number[]')
        descs = request.httprequest.form.getlist('description[]')

        sr_lines = []

        max_len = max(len(models), len(serials), len(descs))

        for i in range(max_len):
            model = (models[i] if i < len(models) else '').strip()
            serial = (serials[i] if i < len(serials) else '').strip()
            desc = (descs[i] if i < len(descs) else '').strip()

            # ✅ Always create row (even if empty)
            sr_lines.append((0, 0, {
                'model_mo': model or False,
                'device_sn': serial or False,
                'description': desc or False,
            }))

        # ticket = request.env['ticket.helpdesk'].sudo().create({
        #     'customer_name': post.get('company_name'),
        #     'subject': post.get('problem_type'),
        #     'description': post.get('description'),
        #     'email': post.get('email'),
        #     'phone': post.get('contact_number'),
        # })

        # models = request.httprequest.form.getlist('model_number[]')
        # serials = request.httprequest.form.getlist('serial_number[]')
        # descs = request.httprequest.form.getlist('device_description[]')

        # for model, serial, desc in zip(models, serials, descs):
        #     if model or serial or desc:
        #         request.env['helpdesk.sr'].sudo().create({
        #             'ticket_id': ticket.id,
        #             'model_mo': model,
        #             'device_sn': serial,
        #             'description': desc,
        #         })
        
        
        ticket = request.env['ticket.helpdesk'].create({
            'customer_id':request.env.user.partner_id.id,
            'company_name': post.get('company_name'),
            'company_address':post.get('company_address'),
            'contact': post.get('contact_person'),
            'store':post.get('store_location'),
            # 'customer_name': post.get('company_name'),
            'subject': post.get('problem_type'),
            'description': post.get('description'),
            'email': post.get('email'),
            'phone': post.get('contact_number'),
            'sr_ids': sr_lines,
        })

        

        files = request.httprequest.files.getlist('attachment')

        for file in files:
            if file:
                request.env['ir.attachment'].sudo().create({
                    'name': file.filename,
                    'datas': base64.b64encode(file.read()),
                    'res_model': 'ticket.helpdesk',
                    'res_id': ticket.id,   # 🔥 LINK HERE
                    'type': 'binary',
                })

        return request.redirect('/my/tickets')
    

    @http.route(['/my/devices'], type='http', auth="user", website=True)
    def my_devices(self, **kwargs):



        partner = request.env.user.partner_id

        devices = request.env['device.inventory'].sudo().search([
            ('end_user_name', '=', partner.id)
        ])

        if request.env.user.show_device_ui:

            return request.render(
                'chainway_helpdesk_custom.portal_device_list',
                {
                    'devices': devices
                }
            )
        
        return request.redirect('/my/tickets')
        
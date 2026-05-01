from odoo import models, fields, api
import random
import string
from odoo import api, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    show_device_ui = fields.Boolean(
        string="Enable Device UI",
        help="Allow user to see Device UI / Views"
    )

    # @api.model
    # def create(self, vals):
    #     user = super().create(vals)

    #     if user.email:
    #         user.action_reset_password()  # generate secure link
    #         template = self.env.ref('chainway_helpdesk_custom.email_template_chainway_user')
    #         template.send_mail(user.id, force_send=True)

    #     return user

    # @api.onchange('show_device_ui')
    # def _onchange_show_device_ui(self):
    #     group = self.env.ref('chainway_helpdesk_custom.group_device_user')

    #     for user in self:
    #         if user.show_device_ui:
    #             user.group_ids |= group
    #         else:
    #             user.group_ids -= group


    @api.onchange('show_device_ui')
    def _onchange_show_device_ui(self):
        group = self.env.ref('chainway_helpdesk_custom.group_device_user')

        for user in self:
            current_groups = user.group_ids.ids

            if user.show_device_ui:
                # add group
                if group.id not in current_groups:
                    user.group_ids = [(6, 0, current_groups + [group.id])]
            else:
                # remove group
                if group.id in current_groups:
                    new_groups = [gid for gid in current_groups if gid != group.id]
                    user.group_ids = [(6, 0, new_groups)]


    


    @api.model_create_multi
    def create(self, vals_list):
        passwords = []
        for vals in vals_list:
            temp_password = self._generate_temp_password()
            vals['password'] = temp_password
            passwords.append(temp_password)

        users = super().create(vals_list)

        for user, temp_password in zip(users, passwords):
            if user.email:
                try:
                    self._send_portal_welcome_email(user, temp_password)
                except Exception as e:
                    self.env['ir.logging'].sudo().create({
                        'name': 'Chainway User Email Error',
                        'type': 'server',
                        'level': 'ERROR',
                        'message': str(e),
                        'path': 'res.users',
                        'func': 'create',
                        'line': '0',
                    })

        return users

    def _send_portal_welcome_email(self, user, temp_password):
        body = """
            <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333; padding: 20px;">
                <p>Dear %s,</p>
                <p>Greetings from <strong>Chainway</strong>!</p>
                <p>We are pleased to introduce our online support interface for logging repair
                requests and technical queries related to our products.</p>
                <p>This portal has been designed to provide you with a quick and convenient way
                to register service requests, track progress, and share technical concerns
                directly with our support team.</p>
                <p><strong>Please find your login details below:</strong></p>
                <table style="border-collapse: collapse; width: 420px; margin: 10px 0;">
                    <tr style="background-color: #f5f5f5;">
                        <td style="padding: 10px 14px; border: 1px solid #ddd; font-weight: bold; width: 140px;">Portal Link</td>
                        <td style="padding: 10px 14px; border: 1px solid #ddd;">
                            <a href="http://38.45.94.141:8070">https://support.chainway.com</a>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 14px; border: 1px solid #ddd; font-weight: bold;">User ID</td>
                        <td style="padding: 10px 14px; border: 1px solid #ddd;">%s</td>
                    </tr>
                    <tr style="background-color: #f5f5f5;">
                        <td style="padding: 10px 14px; border: 1px solid #ddd; font-weight: bold;">Password</td>
                        <td style="padding: 10px 14px; border: 1px solid #ddd;">%s</td>
                    </tr>
                </table>
                <p>We request you to use this interface for all future repair and technical
                support requirements to ensure faster response and better tracking of your
                requests.</p>
                <p>If you face any difficulty accessing the portal or need any assistance,
                please feel free to contact us.</p>
                <p>We look forward to supporting you better through this system.</p>
                <br/>
                <p>Warm Regards,</p>
                <p><strong>Chainway Support Team</strong></p>
            </div>
        """ % (user.name, user.login, temp_password)

        mail = self.env['mail.mail'].sudo().create({
            'subject': 'Access Details for Chainway Support Portal',
            'email_from': self.env.user.email or 'noreply@chainway.com',
            'email_to': user.email,
            'body_html': body,
            'auto_delete': True,
        })
        mail.send()

    def _generate_temp_password(self, length=10):
        chars = string.ascii_letters + string.digits + '!@#$%'
        return ''.join(random.choices(chars, k=length))
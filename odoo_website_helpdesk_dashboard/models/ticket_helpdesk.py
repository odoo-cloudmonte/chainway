# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2026-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
import calendar
from odoo import api, models


class TicketHelpdesk(models.Model):
    """ Inherited class to get help desk ticket details...."""
    _inherit = 'ticket.helpdesk'

    @api.model
    def check_user_group(self):
        """Checking user group"""
        user = self.env.user
        if user.has_group('base.group_user'):
            return True
        return False

#   ============================================================================================

    # @api.model
    # def get_tickets_count(self):
    #     """Function To Get The Ticket Count (Current User Only)"""

    #     user_id = self.env.user.id

    #     # ONLY CURRENT USER TICKETS
    #     domain = [('assigned_user_id', '=', user_id)]

    #     ticket_details = self.search(domain)

    #     ticket_data = [
    #         {
    #             'ticket_name': ticket.name,
    #             'customer_name': ticket.customer_id.name,
    #             'subject': ticket.subject,
    #             'priority': ticket.priority,
    #             'assigned_to': ticket.assigned_user_id.name,
    #             'assigned_image': ticket.assigned_user_id.image_1920,
    #         }
    #         for ticket in ticket_details
    #     ]

    #     # =========================================
    #     # STAGE COUNTS
    #     # =========================================

    #     tickets_new_count = self.search_count([
    #         ('assigned_user_id', '=', user_id),
    #         ('stage_id.name', 'in', ['Inbox', 'Draft', 'New'])
    #     ])

    #     tickets_in_progress_count = self.search_count([
    #         ('assigned_user_id', '=', user_id),
    #         ('stage_id.name', '=', 'In Progress')
    #     ])

    #     tickets_device_recieved_count = self.search_count([
    #         ('assigned_user_id', '=', user_id),
    #         ('stage_id.name', '=', 'Device Received')
    #     ])

    #     tickets_assign_engineer_count = self.search_count([
    #         ('assigned_user_id', '=', user_id),
    #         ('stage_id.name', '=', 'Assign to Engineer')
    #     ])

    #     tickets_pending_count = self.search_count([
    #         ('assigned_user_id', '=', user_id),
    #         ('stage_id.name', '=', 'Pending for Approval')
    #     ])

    #     tickets_dispatch_count = self.search_count([
    #         ('assigned_user_id', '=', user_id),
    #         ('stage_id.name', '=', 'Dispatch')
    #     ])

    #     tickets_cancelled_count = self.search_count([
    #         ('assigned_user_id', '=', user_id),
    #         ('stage_id.name', '=', 'Cancelled')
    #     ])



    #     tickets_done_count = self.search_count([
    #         ('assigned_user_id', '=', user_id),
    #         ('stage_id.name', '=', 'Done')
    #     ])

    #     tickets_closed_count = self.search_count([
    #         ('assigned_user_id', '=', user_id),
    #         ('stage_id.name', '=', 'Closed')
    #     ])



    #     # =========================================
    #     # PRIORITY COUNTS
    #     # =========================================

    #     very_low_count = self.search_count([
    #         ('assigned_user_id', '=', user_id),
    #         ('priority', '=', '0')
    #     ])

    #     low_count = self.search_count([
    #         ('assigned_user_id', '=', user_id),
    #         ('priority', '=', '1')
    #     ])

    #     normal_count = self.search_count([
    #         ('assigned_user_id', '=', user_id),
    #         ('priority', '=', '2')
    #     ])

    #     high_count = self.search_count([
    #         ('assigned_user_id', '=', user_id),
    #         ('priority', '=', '3')
    #     ])

    #     very_high_count = self.search_count([
    #         ('assigned_user_id', '=', user_id),
    #         ('priority', '=', '4')
    #     ])

    #     # =========================================
    #     # PROGRESS VALUES
    #     # =========================================
    #     total_count = very_low_count + low_count + normal_count + high_count + very_high_count

    #     if total_count > 0:
    #         very_low_count1 = (very_low_count / total_count) * 100
    #         low_count1 = (low_count / total_count) * 100
    #         normal_count1 = (normal_count / total_count) * 100
    #         high_count1 = (high_count / total_count) * 100
    #         very_high_count1 = (very_high_count / total_count) * 100
    #     else:
    #         very_low_count1 = 0
    #         low_count1 = 0
    #         normal_count1 = 0
    #         high_count1 = 0
    #         very_high_count1 = 0

    #     # =========================================
    #     # CUSTOMER RESPONSE
    #     # =========================================

    #     response = self.search_count([
    #         ('assigned_user_id', '=', user_id),
    #         ('review', '!=', False)
    #     ])

    #     # =========================================
    #     # TEAM COUNT
    #     # =========================================

    #     teams = self.search([
    #         ('assigned_user_id', '=', user_id),
    #         ('team_id', '!=', False)
    #     ]).mapped('team_id')

    #     teams_count = len(teams)

    #     # =========================================
    #     # PENDING TICKETS
    #     # =========================================

    #     tickets = self.search([
    #         ('assigned_user_id', '=', user_id),
    #         ('stage_id.name', 'in', ['Inbox', 'Draft', 'New'])
    #     ])

    #     p_tickets = [ticket.name for ticket in tickets]

    #     # =========================================
    #     # RETURN
    #     # =========================================

    #     values = {
    #         'new_count': tickets_new_count,
    #         'progress_count': tickets_in_progress_count,
    #         'done_count': tickets_done_count,
    #         'team_count': teams_count,
    #         'p_tickets': p_tickets,
    #         'very_low_count1': very_low_count1,
    #         'low_count1': low_count1,
    #         'normal_count1': normal_count1,
    #         'high_count1': high_count1,
    #         'very_high_count1': very_high_count1,
    #         'response': response,
    #         'ticket_details': ticket_data,
    #         'device_received_count':tickets_device_recieved_count,
    #         'assign_engineer_count': tickets_assign_engineer_count,
    #         'pending_approval_count': tickets_pending_count,
    #         'dispatch_count': tickets_dispatch_count,
    #         'cancelled_count': tickets_cancelled_count,
    #         'closed_count' : tickets_closed_count,
    #     }
    #     return values
    
    # @api.model
    # def action_open_stage(self, stage_name):

    #     return {
    #         'name': stage_name,
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'ticket.helpdesk',
    #         'view_mode': 'tree,form',
    #         'views': [
    #             [False, 'list'],
    #             [False, 'form']
    #         ],
    #         'domain': [
    #             ('stage_id.name', '=', stage_name),
    #             ('assigned_user_id', '=', self.env.user.id)
    #         ],
    #         'context': {
    #             'create': False
    #         },
    #         'target': 'current'
    #     }



    @api.model
    def get_tickets_count(self):
        """Function To Get The Ticket Count"""

        user = self.env.user

        # =========================================
        # DOMAIN BASED ON GROUP
        # =========================================

        if user.has_group('odoo_website_helpdesk.helpdesk_manager'):
            domain = []
        elif user.has_group('odoo_website_helpdesk.helpdesk_team_leader'):
            teams = self.env['team.helpdesk'].search([
                ('team_lead_id', '=', user.id)
            ])
            domain = [('team_id', 'in', teams.ids)]
        else:
            domain = [('assigned_user_id', '=', user.id)]

        ticket_details = self.search(domain)

        ticket_data = [
            {
                'ticket_name': ticket.name,
                'customer_name': ticket.customer_id.name,
                'subject': ticket.subject,
                'priority': ticket.priority,
                'assigned_to': ticket.assigned_user_id.name,
                'assigned_image': ticket.assigned_user_id.image_1920,
            }
            for ticket in ticket_details
        ]

        # =========================================
        # STAGE COUNTS
        # =========================================

        tickets_new_count = self.search_count(
            domain + [('stage_id.name', 'in', ['Inbox', 'Draft', 'New'])]
        )

        tickets_in_progress_count = self.search_count(
            domain + [('stage_id.name', '=', 'In Progress')]
        )

        tickets_device_recieved_count = self.search_count(
            domain + [('stage_id.name', '=', 'Device Received')]
        )

        tickets_assign_engineer_count = self.search_count(
            domain + [('stage_id.name', '=', 'Assign to Engineer')]
        )

        tickets_pending_count = self.search_count(
            domain + [('stage_id.name', '=', 'Pending for Approval')]
        )

        tickets_dispatch_count = self.search_count(
            domain + [('stage_id.name', '=', 'Dispatch')]
        )

        tickets_cancelled_count = self.search_count(
            domain + [('stage_id.name', '=', 'Cancelled')]
        )

        tickets_done_count = self.search_count(
            domain + [('stage_id.name', '=', 'Done')]
        )

        tickets_closed_count = self.search_count(
            domain + [('stage_id.name', '=', 'Closed')]
        )

        # =========================================
        # PRIORITY COUNTS
        # =========================================

        very_low_count = self.search_count(
            domain + [('priority', '=', '0')]
        )

        low_count = self.search_count(
            domain + [('priority', '=', '1')]
        )

        normal_count = self.search_count(
            domain + [('priority', '=', '2')]
        )

        high_count = self.search_count(
            domain + [('priority', '=', '3')]
        )

        very_high_count = self.search_count(
            domain + [('priority', '=', '4')]
        )

        # =========================================
        # PROGRESS VALUES
        # =========================================

        total_count = ( very_low_count + low_count + normal_count + high_count + very_high_count)

        if total_count > 0:
            very_low_count1 = (very_low_count / total_count) * 100
            low_count1 = (low_count / total_count) * 100
            normal_count1 = (normal_count / total_count) * 100
            high_count1 = (high_count / total_count) * 100
            very_high_count1 = (very_high_count / total_count) * 100
        else:
            very_low_count1 = 0
            low_count1 = 0
            normal_count1 = 0
            high_count1 = 0
            very_high_count1 = 0

        # =========================================
        # CUSTOMER RESPONSE
        # =========================================

        response = self.search_count(
            domain + [('review', '!=', False)]
        )

        # =========================================
        # TEAM COUNT
        # =========================================

        teams = self.search(
            domain + [('team_id', '!=', False)]
        ).mapped('team_id')

        teams_count = len(teams)

        # =========================================
        # PENDING TICKETS
        # =========================================

        tickets = self.search(
            domain + [('stage_id.name', 'in', ['Inbox', 'Draft', 'New'])]
        )

        p_tickets = [ticket.name for ticket in tickets]

        # =========================================
        # RETURN
        # =========================================

        values = {
            'new_count': tickets_new_count,
            'progress_count': tickets_in_progress_count,
            'done_count': tickets_done_count,
            'team_count': teams_count,
            'p_tickets': p_tickets,
            'very_low_count1': very_low_count1,
            'low_count1': low_count1,
            'normal_count1': normal_count1,
            'high_count1': high_count1,
            'very_high_count1': very_high_count1,
            'response': response,
            'ticket_details': ticket_data,
            'device_received_count': tickets_device_recieved_count,
            'assign_engineer_count': tickets_assign_engineer_count,
            'pending_approval_count': tickets_pending_count,
            'dispatch_count': tickets_dispatch_count,
            'cancelled_count': tickets_cancelled_count,
            'closed_count': tickets_closed_count,
        }

        return values


    @api.model
    def action_open_stage(self, stage_name):

        user = self.env.user

        # =========================================
        # DOMAIN BASED ON GROUP
        # =========================================

        domain = [
            ('stage_id.name', '=', stage_name)
        ]

        # if not user.has_group('odoo_website_helpdesk.helpdesk_manager'):
        #     domain.append(
        #         ('assigned_user_id', '=', user.id)
        #     )
        
        if user.has_group('odoo_website_helpdesk.helpdesk_manager'):
            pass

        elif user.has_group('odoo_website_helpdesk.helpdesk_team_leader'):
            teams = self.env['team.helpdesk'].search([
                ('team_lead_id', '=', user.id)
            ])

            # Option 1: Show all tickets belonging to the leader's teams
            domain.append(('team_id', 'in', teams.ids))

            # OR Option 2: Show tickets assigned to the leader and team members
            # users = teams.member_ids | teams.team_lead_id
            # domain.append(('assigned_user_id', 'in', users.ids))

        else:
            domain.append(('assigned_user_id', '=', user.id))

        return {
            'name': stage_name,
            'type': 'ir.actions.act_window',
            'res_model': 'ticket.helpdesk',
            'view_mode': 'list,form',
            'views': [
                [False, 'list'],
                [False, 'form']
            ],
            'domain': domain,
            'context': {
                'create': False
            },
            'target': 'current'
        }

    @api.model
    def get_tickets_view(self):
        """ Function To Get The Ticket View"""
        tickets_new_count = self.search_count(
            [('stage_id.name', 'in', ['Inbox', 'Draft','New'])])
        tickets_in_progress_count = self.search_count(
            [('stage_id.name', '=', 'In Progress')])
        tickets_closed_count = self.search_count(
            [('stage_id.name', '=', 'Done')])
        teams_count = self.search_count([])
        tickets_new = self.search(
            [('stage_id.name', 'in', ['Inbox', 'Draft','New'])])
        tickets_in_progress = self.search(
            [('stage_id.name', '=', 'In Progress')])
        tickets_closed = self.search(
            [('stage_id.name', '=', 'Done')])
        teams = self.env['team.helpdesk'].search([])
        new_list = [f"{new.name} : {new.subject}" for new in tickets_new]
        progress_list = [f"{progress.name} : {progress.subject}" for progress in
                         tickets_in_progress]
        done_list = [f"{done.name} : {done.subject}" for done in tickets_closed]
        teams_list = [team.name for team in teams]

        tickets = self.search(
            [('stage_id.name', 'in', ['Inbox', 'Draft','New'])])
        p_tickets = [ticket.name for ticket in tickets]
        values = {
            'inbox_count': tickets_new_count,
            'progress_count': tickets_in_progress_count,
            'done_count': tickets_closed_count,
            'team_count': teams_count,
            'new_tkts': new_list,
            'progress': progress_list,
            'done': done_list,
            'teams': teams_list,
            'p_tickets': p_tickets
        }
        return values

    @api.model
    def get_ticket_month_pie(self):
        """For pie chart"""
        month_count = []
        month_value = []
        tickets = self.search([])
        for rec in tickets:
            month = rec.create_date.month
            if month not in month_value:
                month_value.append(month)
            month_count.append(month)
        month_val = []
        for index in range(len(month_value)):
            value = month_count.count(month_value[index])
            month_name = calendar.month_name[month_value[index]]
            month_val.append({'label': month_name, 'value': value})
        name = [record.get('label') for record in month_val]
        count = [record.get('value') for record in month_val]
        month = [count, name]
        return month

    

#  ==================================================================

    # @api.model
    # def get_team_ticket_count_pie(self):
    #     """Bar chart - Only current user's assigned tickets"""

    #     ticket_count = []
    #     team_list = []

    #     # ONLY CURRENT USER ASSIGNED TICKETS
    #     tickets = self.search([
    #         ('assigned_user_id', '=', self.env.user.id)
    #     ])

    #     for rec in tickets:

    #         if rec.team_id:

    #             team = rec.team_id.name

    #             if team not in team_list:
    #                 team_list.append(team)

    #             ticket_count.append(team)

    #     team_val = []

    #     for index in range(len(team_list)):

    #         value = ticket_count.count(team_list[index])

    #         team_name = team_list[index]

    #         team_val.append({
    #             'label': team_name,
    #             'value': value
    #         })

    #     name = [record.get('label') for record in team_val]

    #     count = [record.get('value') for record in team_val]

    #     return [count, name]
    
    # def get_stage_domain(self, stage_name):
    #     return [
    #         ('stage_id.name', '=', stage_name),
    #         ('assigned_user_id', '=', self.env.user.id)
    #     ]

    @api.model
    def get_team_ticket_count_pie(self):
        """Pie chart - Team wise ticket count"""

        user = self.env.user

        # =========================================
        # DOMAIN BASED ON GROUP
        # =========================================

        domain = []

        if not user.has_group('odoo_website_helpdesk.helpdesk_manager'):
            domain.append(
                ('assigned_user_id', '=', user.id)
            )

        ticket_count = []
        team_list = []

        tickets = self.search(domain)

        for rec in tickets:

            if rec.team_id:

                team = rec.team_id.name

                if team not in team_list:
                    team_list.append(team)

                ticket_count.append(team)

        team_val = []

        for index in range(len(team_list)):

            value = ticket_count.count(team_list[index])

            team_name = team_list[index]

            team_val.append({
                'label': team_name,
                'value': value
            })

        name = [record.get('label') for record in team_val]

        count = [record.get('value') for record in team_val]

        return [count, name]


    def get_stage_domain(self, stage_name):

        domain = [
            ('stage_id.name', '=', stage_name)
        ]

        # =========================================
        # MANAGER CAN SEE ALL TICKETS
        # =========================================

        if not self.env.user.has_group('odoo_website_helpdesk.helpdesk_manager'):
            domain.append(
                ('assigned_user_id', '=', self.env.user.id)
            )

        return domain
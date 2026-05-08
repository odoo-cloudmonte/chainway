/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { _t } from "@web/core/l10n/translation";
import { Component } from "@odoo/owl";
import { onMounted, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { session } from "@web/session";

/** HelpDesk Dashboard **/

class HelpDeskDashBoard extends Component {

    setup() {
        super.setup();

        this.ref = useRef("helpDeskDashboard");
        this.actionService = useService("action");

        onMounted(this.onMounted);
    }

    /** Mounted **/

    onMounted() {
        this.render_dashboards();
        this.render_graphs();
    }

    /** =========================================
     *  DASHBOARD COUNTS
     * ========================================= */

    render_dashboards() {

        var self = this;

        rpc('/web/dataset/call_kw/ticket.helpdesk/get_tickets_count', {
            model: 'ticket.helpdesk',
            method: 'get_tickets_count',
            args: [],
            kwargs: {},
        }).then(function(result) {

            /** SAFE SETTER **/

            function setCount(id, value) {

                const el = self.ref.el.querySelector(id);

                if (el) {
                    el.innerHTML = value || 0;
                }
            }

            /** STAGE COUNTS **/
            debugger;
            setCount('#new_count', result.new_count);
            setCount('#inprogress_count', result.progress_count);
            setCount('#device_received_count', result.device_received_count);
            setCount('#assign_engineer_count', result.assign_engineer_count);
            setCount('#pending_approval_count', result.pending_approval_count);
            setCount('#dispatch_count', result.dispatch_count);
            setCount('#cancelled_count', result.cancelled_count);
            setCount('#done_count', result.done_count);
            setCount('#closed_count', result.closed_count);

            /** CUSTOMER RESPONSE **/

            $(".response").empty().append(result.response || 0);

            /** PRIORITY BARS **/

            var priorityCounts = {
                very_low: result.very_low_count1 || 0,
                low: result.low_count1 || 0,
                normal: result.normal_count1 || 0,
                high: result.high_count1 || 0,
                very_high: result.very_high_count1 || 0
            };

            for (var priority in priorityCounts) {

                $("." + priority + "_count").empty();

                var progressBarWidth = priorityCounts[priority] + "%";

                var progressBar = $("<div class='progress-bar'></div>")
                    .css({
                        "width": progressBarWidth,
                        "height": "12px",
                        "border-radius": "20px",
                        "background": "linear-gradient(90deg,#6366f1,#8b5cf6)"
                    });

                var progressBarContainer = $("<div class='progress'></div>")
                    .css({
                        "background": "#e5e7eb",
                        "border-radius": "20px",
                        "overflow": "hidden",
                        "height": "12px"
                    })
                    .append(progressBar);

                var progressValue = $("<div class='progress-value'></div>")
                    .text(priorityCounts[priority] + "%")
                    .css({
                        "margin-top": "6px",
                        "font-size": "13px",
                        "font-weight": "600",
                        "color": "#475569"
                    });

                $("." + priority + "_count").append(progressBarContainer);
                $("." + priority + "_count").append(progressValue);
            }

        });
    }

    /** =========================================
     *  RENDER CHARTS
     * ========================================= */

    render_graphs() {

        this.render_tickets_month_graph();
        this.render_team_ticket_count_graph();
    }

    /** =========================================
     *  DOUGHNUT CHART
     * ========================================= */

    render_tickets_month_graph() {

        var self = this;

        var ctx = this.ref.el.querySelector('#ticket_month');

        if (!ctx) {
            return;
        }

        rpc('/web/dataset/call_kw/ticket.helpdesk/get_tickets_count', {
            model: "ticket.helpdesk",
            method: "get_tickets_view",
            args: [],
            kwargs: {},
        }).then(function(values) {

            var data = {

                labels: [
                    'New',
                    'In Progress',
                    'Device Received',
                    'Assign Engineer',
                    'Pending Approval',
                    'Dispatch',
                    'Cancelled',
                    'Done',
                    'Closed'
                ],

                datasets: [{
                    data: [
                        values.new_count || 0,
                        values.progress_count || 0,
                        values.device_received_count || 0,
                        values.assign_engineer_count || 0,
                        values.pending_approval_count || 0,
                        values.dispatch_count || 0,
                        values.cancelled_count || 0,
                        values.done_count || 0,
                        values.closed_count || 0
                    ],

                    backgroundColor: [
                        "#ec4899",
                        "#f59e0b",
                        "#8b5cf6",
                        "#3b82f6",
                        "#6366f1",
                        "#14b8a6",
                        "#ef4444",
                        "#10b981",
                        "#334155"
                    ],

                    borderWidth: 1
                }]
            };

            var options = {

                responsive: true,

                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            };

            new Chart(ctx, {
                type: "doughnut",
                data: data,
                options: options
            });
        });
    }

    /** =========================================
     *  TEAM BAR CHART
     * ========================================= */

    render_team_ticket_count_graph() {

        var self = this;

        var ctx = this.ref.el.querySelector('.team_ticket_count');

        if (!ctx) {
            return;
        }

        rpc('/web/dataset/call_kw/ticket.helpdesk/get_tickets_count', {
            model: "ticket.helpdesk",
            method: "get_team_ticket_count_pie",
            args: [],
            kwargs: {},
        }).then(function(arrays) {

            var data = {

                labels: arrays[1],

                datasets: [{
                    label: "Tickets",

                    data: arrays[0],

                    backgroundColor: [
                        'rgba(255, 99, 132, 0.5)',
                        'rgba(255, 159, 64, 0.5)',
                        'rgba(255, 205, 86, 0.5)',
                        'rgba(75, 192, 192, 0.5)',
                        'rgba(54, 162, 235, 0.5)',
                        'rgba(153, 102, 255, 0.5)',
                        'rgba(201, 203, 207, 0.5)'
                    ],

                    borderWidth: 1
                }]
            };

            var options = {

                responsive: true,

                plugins: {
                    legend: {
                        display: false
                    }
                },

                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            };

            new Chart(ctx, {
                type: "bar",
                data: data,
                options: options
            });
        });
    }

    /** =========================================
     *  COMMON STAGE ACTION
     * ========================================= */

    // open_stage(ev, stageName) {

    //     ev.stopPropagation();
    //     ev.preventDefault();
    //     debugger;

    //     this.actionService.doAction({

    //         name: _t(stageName),

    //         type: 'ir.actions.act_window',

    //         res_model: 'ticket.helpdesk',

    //         view_mode: 'tree,form',

    //         views: [
    //             [false, 'list'],
    //             [false, 'form']
    //         ],
            
    //         domain: [['stage_id.name', '=', stageName]],

    //         context: {
    //             create: false
    //         },

    //         target: 'current'
    //     });
    // }

    open_stage(ev, stageName) {

    ev.stopPropagation();
    ev.preventDefault();

    const self = this;

    rpc('/web/dataset/call_kw', {

        model: 'ticket.helpdesk',

        method: 'action_open_stage',

        args: [stageName],

        kwargs: {}

    }).then(function(action) {

        self.actionService.doAction(action);

    });
}

    /** =========================================
     *  STAGE METHODS
     * ========================================= */

    tickets_new(ev) {
        this.open_stage(ev, "New");
    }

    tickets_inprogress(ev) {
        this.open_stage(ev, "In Progress");
    }

    tickets_device_received(ev) {
        this.open_stage(ev, "Device Received");
    }

    tickets_assign_engineer(ev) {
        this.open_stage(ev, "Assign to Engineer");
    }

    tickets_pending_approval(ev) {
        this.open_stage(ev, "Pending for Approval");
    }

    tickets_dispatch(ev) {
        this.open_stage(ev, "Dispatch");
    }

    tickets_cancelled(ev) {
        this.open_stage(ev, "Cancelled");
    }

    tickets_done(ev) {
        this.open_stage(ev, "Done");
    }

    tickets_closed(ev) {
        this.open_stage(ev, "Closed");
    }

    /** =========================================
     *  HELPDESK TEAMS
     * ========================================= */

    helpdesk_teams(ev) {

        ev.stopPropagation();
        ev.preventDefault();

        this.actionService.doAction({

            name: _t("Teams"),

            type: 'ir.actions.act_window',

            res_model: 'team.helpdesk',

            view_mode: 'tree,form',

            views: [
                [false, 'list'],
                [false, 'form']
            ],

            target: 'current'
        });
    }
}

/** TEMPLATE **/

HelpDeskDashBoard.template = 'DashBoardHelpDesk';

/** REGISTER ACTION **/

registry.category("actions").add(
    "helpdesk_dashboard",
    HelpDeskDashBoard
);
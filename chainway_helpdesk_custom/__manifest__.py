{
    'name': 'Device Inventory Management',
    'version': '1.0',
    'depends': ['base', 'mail','odoo_website_helpdesk','web'],
    'data': [
        'security/ir.model.access.csv',
        'data/cron.xml',
        'views/device_inventory_views.xml',
        'views/device_inventory_menu.xml',
        'views/warrenty_form.xml',
        'views/helpdesk_inherit_view.xml',
        # 'views/helpdesk_from.xml',
        'views/helpdesk_ui.xml',
        'views/res_user_inherit_view.xml',
        'views/portal_device_list.xml',
        'views/export_import_wizard.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'chainway_helpdesk_custom/static/src/js/main.js',
        ],
    },
    'installable': True,
    'application': True,
}
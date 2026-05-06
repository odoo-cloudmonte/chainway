# -*- coding: utf-8 -*-
{
    'name': 'Image Link Generator',
    'version': '1.0',
    'summary': 'Store image and generate public hyperlink',
    'category': 'Tools',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/image_record_views.xml',
    ],
    'installable': True,
    'application': True,
}
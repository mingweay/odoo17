# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['base'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'data':[
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'views/estate_menus.xml',

    ]
}
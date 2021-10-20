# -*- coding: utf-8 -*-
# Copyright 2020 Subteno IT
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': "auth_oauth_azure",
    'summary': """
Allow users to login through Microsoft Azure Provider.
=============================================
        """,
    'author': "Subteno",
    'website': "https://www.subteno.com",
    'category': 'Hidden/Tools',
    'version': '0.1',
    'depends': [
        'base',
        'auth_oauth'
    ],
    'data': [
        'data/auth_oauth_data.xml',
        'views/auth_oauth_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'auth_oauth_azure/static/**/*',
        ],
    },
    'license': 'LGPL-3',
}

# -*- coding: utf-8 -*-
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
        'views/auth_oauth_templates.xml',
        'views/auth_oauth_views.xml',
        'views/res_config_settings_views.xml',
    ],
}

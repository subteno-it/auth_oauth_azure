# -*- coding: utf-8 -*-
# Copyright 2020 Subteno IT
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AuthOAuthProvider(models.Model):
    """Class defining the configuration values of an OAuth2 provider"""

    _inherit = 'auth.oauth.provider'

    client_secret = fields.Char(string='Client Secret')
    response_type = fields.Selection([('token', 'Token'), ('code', 'Code')], default='token', required=True)

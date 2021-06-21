# -*- coding: utf-8 -*-
# Copyright 2020 Subteno IT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
import werkzeug

from odoo.http import request
from odoo.addons.auth_oauth.controllers.main import OAuthLogin


class OAuthLogin(OAuthLogin):
    def list_providers(self):
        try:
            providers = request.env['auth.oauth.provider'].sudo().search_read([('enabled', '=', True)])
        except Exception:
            providers = []
        for provider in providers:
            return_url = request.httprequest.url_root + 'auth_oauth/signin'
            state = self.get_state(provider)
            params = dict(
                response_type=provider['response_type'],
                client_id=provider['client_id'],
                redirect_uri=return_url,
                scope=provider['scope'],
                state=json.dumps(state),
            )
            provider['auth_link'] = "%s?%s" % (provider['auth_endpoint'], werkzeug.urls.url_encode(params))
        return providers

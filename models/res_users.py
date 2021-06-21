# -*- coding: utf-8 -*-
# Copyright 2020 Subteno IT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


import logging
import requests

from odoo.http import request

from odoo import api, models
from odoo.exceptions import AccessDenied

from odoo.addons import base
base.models.res_users.USER_PRIVATE_FIELDS.append('oauth_access_token')

_logger = logging.getLogger(__name__)

try:
    import jwt
except ImportError:
    _logger.warning("The PyJWT python library is not installed, login with Microsoft OAuth2 won't be available.")
    jwt = None


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _auth_oauth_code_validate(self, provider, code):
        """ requests access_token using provided code and returns
            the validation data corresponding to the access token
        """
        oauth_provider = self.env['auth.oauth.provider'].browse(provider)
        req_params = dict(
            client_id=oauth_provider.client_id,
            client_secret=oauth_provider.client_secret,
            grant_type='authorization_code',
            code=code,
            redirect_uri=request.httprequest.url_root + 'auth_oauth/signin',
        )
        headers = {'Accept': 'application/json'}

        token_info = requests.post(oauth_provider.validation_endpoint, headers=headers, data=req_params).json()
        if token_info.get("error"):
            raise Exception(token_info['error'])

        access_token = token_info.get('access_token')
        validation = {
            'access_token': access_token
        }

        if token_info.get('id_token'):
            # Used in case of Microsoft's Azure AD API
            # We can directly access basic info from 'id_token', without
            # making another call to any data_endpoint
            if not jwt:
                _logger.warning("The PyJWT python library is missing, not able to login with Microsoft Account.")
                raise AccessDenied()
            data = jwt.decode(token_info['id_token'], options={"verify_signature": False})
        else:
            # For other providers, fetch data using data_endpoint
            data = self._auth_oauth_rpc(oauth_provider.data_endpoint, access_token)

        validation.update(data)
        return validation

    @api.model
    def auth_oauth(self, provider, params):
        # Advice by Google (to avoid Confused Deputy Problem)
        # if validation.audience != OUR_CLIENT_ID:
        #   abort()
        # else:
        #   continue with the process
        if params.get('code'):
            # code grant flow, which will give code to retrieve access_token
            validation = self._auth_oauth_code_validate(provider, params['code'])
            access_token = validation.pop('access_token')
            params['access_token'] = access_token
        else:
            # implicit flow, which directly gives access_token
            access_token = params.get('access_token')
            validation = self._auth_oauth_validate(provider, access_token)
        # required check
        if not validation.get('user_id'):
            # Workaround for Facebook and Microsoft as they do not send 'user_id'
            if validation.get('id'):  # for Facebook
                validation['user_id'] = validation['id']
            elif validation.get('oid'):  # for Microsoft
                validation['user_id'] = validation['oid']
            else:
                raise AccessDenied()

        # retrieve and sign in user
        login = self._auth_oauth_signin(provider, validation, params)
        if not login:
            raise AccessDenied()
        # return user credentials
        return (self.env.cr.dbname, login, access_token)

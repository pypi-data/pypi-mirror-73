"""
Base Implementation of the ZengaPay API client

@author: Patrick Walukagga
"""


import json

import requests
from requests import Request, Session
from requests.auth import AuthBase

from .config import ZengaPayConfig
from .utils import requests_retry_session

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError


class Response:
    def __init__(self, body, code, headers):
        self.body = body
        self.code = code
        self.headers = headers
        self.data = body


class ZengaPayAuth(AuthBase):
    """Attaches Authentation to the given Requesst Object."""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        """Attach an API user token to a custom auth header."""

        # Modify and return the request
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r


class ClientInterface:
    def get_auth_token(self):
        raise NotImplementedError

    def get_transaction_status(self):
        return NotImplementedError


class Client(ClientInterface):
    def get_auth_token(self):
        return super(Client, self).get_auth_token()

    def get_transaction_status(self):
        return super(Client, self).get_transaction_status()


class ZengaPayAPI(ClientInterface):
    def __init__(self, config, **kwargs):
        super(ZengaPayAPI, self).__init__(**kwargs)
        self._session = Session()
        self._config = ZengaPayConfig(config)

    @property
    def config(self):
        return self._config

    def request(self, method, url, post_data=None):
        self.auth_token = self.get_auth_token()
        request = Request(
            method, url, data=post_data, auth=ZengaPayAuth(self.auth_token)
        )

        prep_req = self._session.prepare_request(request)
        resp = requests_retry_session(session=self._session).send(
            prep_req, verify=False
        )

        return resp

    def get_auth_token(self):
        return self.config.api_token

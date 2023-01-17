import platform
import re
import time
from collections import OrderedDict

from requests import Request, Session
from .resources import Order, Shipment, Stock
from .exceptions import ServerError, BadRequest, AuthenticationError


class EwhsClient:
    UNAME = " ".join(platform.uname())
    CLIENT_VERSION = "0.1.1"

    API_URL = "https://eu.middleware.ewarehousing-solutions.com"

    def __init__(self, username, password, customer_code=None, wms_code=None, api_url=None):
        self.session = Session()

        self.username = username
        self.password = password
        self.customer_code = customer_code
        self.wms_code = wms_code
        self.access_token = None
        self.refresh_token = None
        self.expires_at = 0

        self._url = api_url if api_url else self.API_URL

        self.user_agent_components = OrderedDict()
        self.set_user_agent_component("Ewarehousing", self.CLIENT_VERSION)
        self.set_user_agent_component("Python", platform.python_version())

        # initialize resources
        self.shipment = Shipment(self)
        self.order = Order(self)
        self.stock = Stock(self)

    def set_user_agent_component(self, key, value, sanitize=True):
        """Add or replace new user-agent component strings.

        Given strings are formatted along the format agreed upon by eWarehousing and implementers:
        - key and values are separated by a forward slash ("/").
        - multiple key/values are separated by a space.
        - keys are camel-cased, and cannot contain spaces.
        - values cannot contain spaces.

        Note: When you set sanitize=false you need to make sure the formatting is correct yourself.
        """
        if sanitize:
            key = "".join(_x.capitalize() for _x in re.findall(r"\S+", key))
            if re.search(r"\s+", value):
                value = "_".join(re.findall(r"\S+", value))
        self.user_agent_components[key] = value

    @property
    def user_agent(self):
        """Return the formatted user agent string."""
        components = ["/".join(x) for x in self.user_agent_components.items()]
        return " ".join(components)

    def _send(self, method, resource, resource_id=None, data=None, params=None, expand=None, **kwargs):
        url = 'wms/{}'.format(resource)

        if resource_id is not None:
            url = '{}/{}'.format(url, resource_id)

        self._authenticate()

        headers = dict(self._get_headers(), **{"Authorization": "Bearer {}".format(self.access_token)})

        if expand and len(expand):
            headers['Expand'] = ','.join(expand)

        request = Request(
            method=method,
            url=self._format_url(url),
            json=data,
            params=params,
            headers=headers,
        )

        prepped = self.session.prepare_request(request=request)
        response = self.session.send(prepped)

        if response.status_code == 401:
            raise AuthenticationError(response.json())

        if response.status_code == 400:
            raise BadRequest()

        if response.status_code == 500:
            raise ServerError()

        if response.status_code == 204:
            return None

        return response.json()

    def _authenticate(self):
        if not self.access_token or int(time.time()) > self.expires_at:
            self.request_access_token()

    def request_access_token(self):
        if not self.refresh_token:
            return self.request_refresh_token()

        auth_url = "wms/auth/refresh/"

        self._send_auth(
            auth_url,
            {"refresh_token": self.refresh_token},
        )

    def request_refresh_token(self):
        auth_url = "wms/auth/login/"

        self._send_auth(
            auth_url,
            {
                "username": self.username,
                "password": self.password
            },
        )

    def _send_auth(self, url, post_data):
        request = Request(
            method="POST",
            url=self._format_url(url),
            json=post_data,
            headers=self._get_headers(),
        )

        prepped = self.session.prepare_request(request=request)
        response = self.session.send(prepped)
        data = response.json()

        if response.status_code != 200:
            raise AuthenticationError(data["message"])

        self.refresh_token = data["refresh_token"]
        self.access_token = data["token"]
        self.expires_at = data["exp"]

    def _get_default_headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": self.user_agent,
            "X-Ewhs-Client-Info": self.UNAME,
        }

    def _get_headers(self):
        headers = self._get_default_headers()

        if self.customer_code:
            headers["X-Customer-Code"] = self.customer_code

        if self.wms_code:
            headers["X-Wms-Code"] = self.wms_code

        return headers

    def _format_url(self, url):
        url = "{}/{}".format(self._url, url)

        if not url.endswith("/"):
            return url + "/"

        return url

    def filter(self, resource, params=None, expand=None, **kwargs):
        return self._send('GET', resource, params=params, expand=expand, **kwargs)

    def create(self, resource, data, expand=None, **kwargs):
        return self._send('POST', resource, data=data, expand=expand, **kwargs)

    def update(self, resource, resource_id, data, expand=None, **kwargs):
        return self._send('PATCH', resource, resource_id, data=data, expand=expand, **kwargs)

    def delete(self, resource, resource_id, expand=None, **kwargs):
        return self._send('DELETE', resource, resource_id, expand=expand, **kwargs)

    def get(self, resource, resource_id, expand=None, **kwargs):
        return self._send('GET', resource, resource_id, expand=expand, **kwargs)

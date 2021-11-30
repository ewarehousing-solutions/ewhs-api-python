import platform
import re
from collections import OrderedDict

from requests import Request, Session
from requests.auth import HTTPBasicAuth
from .resources import Order, Shipment
from .exceptions import ServerError, BadRequest


class EwhsClient:
    UNAME = " ".join(platform.uname())
    CLIENT_VERSION = "0.1.0"

    API_URL = "https://api.ewarehousing.com/api"

    def __init__(self, username, password, customer_id, api_url=None):
        self.session = Session()

        self.username = username
        self.password = password
        self.customer_id = customer_id

        self._url = api_url if api_url else self.API_URL

        self.user_agent_components = OrderedDict()
        self.set_user_agent_component("Ewarehousing", self.CLIENT_VERSION)
        self.set_user_agent_component("Python", platform.python_version())

        # initialize resources
        self.shipment = Shipment(self)
        self.order = Order(self)

    def set_user_agent_component(self, key, value, sanitize=True):
        """Add or replace new user-agent component strings.

        Given strings are formatted along the format agreed upon by Mollie and implementers:
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

    def _send(self, method, resource, resource_id=None, data=None, params=None, **kwargs):
        url = '{}/{}'.format(self._url, resource)

        if resource_id is not None:
            url = '{}/{}'.format(url, resource_id)

        self._authenticate()

        auth = HTTPBasicAuth(self.username, self.password)

        request = Request(
            method=method,
            url=url,
            json=data,
            params=params,
            auth=auth,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
                "X-Ewhs-Client-Info": self.UNAME,
            },
        )

        prepped = self.session.prepare_request(request=request)
        response = self.session.send(prepped)

        if response.status_code == 400:
            raise BadRequest()

        if response.status_code == 500:
            raise ServerError()

        if response.status_code == 204:
            return None

        return response.json()

    def filter(self, resource, params=None, **kwargs):
        return self._send('GET', resource, params=params, **kwargs)

    def create(self, resource, data, **kwargs):
        return self._send('POST', resource, data=data, **kwargs)

    def update(self, resource, resource_id, data, **kwargs):
        return self._send('PUT', resource, resource_id, data=data, **kwargs)

    def delete(self, resource, resource_id, **kwargs):
        return self._send('DELETE', resource, resource_id, **kwargs)

    def get(self, resource, resource_id, **kwargs):
        return self._send('GET', resource, resource_id, **kwargs)

    def _authenticate(self):
        # to implement
        pass
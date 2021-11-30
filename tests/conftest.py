import os
import pytest
import responses
from ewhs.client import EwhsClient


@pytest.fixture(scope="session")
def client():
    client = EwhsClient("test", "testpassword", "9fc05c82-0552-4ca5-b588-c64d77f117a9")
    return client

class ImprovedRequestsMock(responses.RequestsMock):
    """Wrapper adding a few shorthands to responses.RequestMock."""

    def get(self, url, filename, status=200):
        """Setup a mock response for a GET request."""
        body = self._get_body(filename)
        self.add(responses.GET, url, body=body, status=status, content_type="application/json")

    def post(self, url, filename, status=200):
        """Setup a mock response for a POST request."""
        body = self._get_body(filename)
        self.add(responses.POST, url, body=body, status=status, content_type="application/json")

    def delete(self, url, filename, status=204):
        """Setup a mock response for a DELETE request."""
        body = self._get_body(filename)
        self.add(responses.DELETE, url, body=body, status=status, content_type="application/json")

    def patch(self, url, filename, status=200):
        """Setup a mock response for a PATCH request."""
        body = self._get_body(filename)
        self.add(responses.PATCH, url, body=body, status=status, content_type="application/json")

    def _get_body(self, filename):
        """Read the response fixture file and return it."""
        file = os.path.join(os.path.dirname(__file__), "responses", f"{filename}.json")
        with open(file, encoding="utf-8") as f:
            return f.read()


@pytest.fixture
def response():
    """Setup the responses fixture."""
    with ImprovedRequestsMock() as mock:
        yield mock

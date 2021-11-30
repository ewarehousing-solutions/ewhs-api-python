import re


def test_client_default_user_agent(client, response):
    """Default user-agent should contain some known values."""
    regex = re.compile(r"^Ewarehousing/[\d\.]+ Python/[\w\.\+]+$")
    assert re.match(regex, client.user_agent)

    # perform a request and inpect the actual used headers
    response.get("https://api.ewarehousing.com/api/orders", "order_list")
    client.order.list()
    request = response.calls[0].request
    assert re.match(regex, request.headers["User-Agent"])

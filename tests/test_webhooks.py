def test_list_webhooks(authenticated_client, response):
    """Retrieve a list of webhooks"""
    response.get(f"https://eu.middleware.ewarehousing-solutions.com/webhooks/", "webhook_list")

    webhooks = authenticated_client.webhook.list()
    assert isinstance(webhooks, dict)
    assert webhooks['results'] != None
    #
    assert isinstance(webhooks['results'], list)
    assert len(webhooks['results']) == 2
    #
    assert webhooks['results'][0]['group'] == 'stock'
    assert webhooks['results'][0]['action'] == 'updated'


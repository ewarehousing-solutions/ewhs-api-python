def test_list_shipping_methods(authenticated_client, response):
    """Retrieve a list of shipments"""
    response.get(f"https://eu.middleware.ewarehousing-solutions.com/wms/shippingmethods/", "shipping_methods_list")

    shipping_methods = authenticated_client.shipping_methods.list()
    assert isinstance(shipping_methods, list)

    assert len(shipping_methods) == 1

    assert shipping_methods[0]['id'] == '1ef28ca7-8437-65a4-a768-63d61c99510d'
    assert shipping_methods[0]['shipper'] == 'Bol'
    assert shipping_methods[0]['shipper_code'] == 'bol'
    assert shipping_methods[0]['code'] == 'VVB'
    assert shipping_methods[0]['description'] == 'Verzenden via Bol.com'
    assert shipping_methods[0]['shipping_software'] == 'vvb'


def test_filter_shipping_methods(authenticated_client, response):
    """Retrieve a list of filtered shipping_methods"""
    response.get("https://eu.middleware.ewarehousing-solutions.com/wms/shippingmethods/?code=VVB", "shipping_methods_list")

    shipping_methods = authenticated_client.shipping_methods.list(params={
        'code': 'VVB',
    })

    assert isinstance(shipping_methods, list)

    assert len(shipping_methods) == 1

    assert shipping_methods[0]['id'] == '1ef28ca7-8437-65a4-a768-63d61c99510d'
    assert shipping_methods[0]['shipper'] == 'Bol'
    assert shipping_methods[0]['shipper_code'] == 'bol'
    assert shipping_methods[0]['code'] == 'VVB'
    assert shipping_methods[0]['description'] == 'Verzenden via Bol.com'
    assert shipping_methods[0]['shipping_software'] == 'vvb'


def test_get_shipping_method(authenticated_client, response):
    """Retrieve a single shipping_method by shipping_method ID."""
    response.get(
        f"https://eu.middleware.ewarehousing-solutions.com/wms/shippingmethods/1ef28ca7-8437-65a4-a768-63d61c99510d/",
        "shipping_methods_single")

    shipping_method = authenticated_client.shipping_methods.get('1ef28ca7-8437-65a4-a768-63d61c99510d')
    assert isinstance(shipping_method, dict)

    assert shipping_method['id'] == '1ef28ca7-8437-65a4-a768-63d61c99510d'
    assert shipping_method['shipper'] == 'Bol'
    assert shipping_method['shipper_code'] == 'bol'
    assert shipping_method['code'] == 'VVB'
    assert shipping_method['description'] == 'Verzenden via Bol.com'
    assert shipping_method['shipping_software'] == 'vvb'

def test_list_shipments(authenticated_client, response):
    """Retrieve a list of shipments"""
    response.get(f"https://api.ewarehousing.com/wms/shipments", "shipment_list")

    shipments = authenticated_client.shipment.list()
    assert isinstance(shipments, list)

    assert len(shipments) == 1

    assert shipments[0]['id'] == '1701bf71-0b9a-4984-bee5-c9e83b7d2c1d'
    assert shipments[0]['order_reference'] == 'MW_ORD_001'
    assert shipments[0]['labels'][0]['tracking_code'] == 'ewh-pick-up'
    assert shipments[0]['labels'][0]['tracking_url'] == '#'
    assert shipments[0]['labels'][0]['shipping_method']['id'] == '7e808ac8-4167-11e9-92f0-0242ac140006'
    assert shipments[0]['labels'][0]['shipping_method']['name'] == 'eWarehousing afhaal order'


def test_filter_shipments(authenticated_client, response):
    """Retrieve a list of shipments"""
    response.get("https://api.ewarehousing.com/wms/shipments?order_reference=VB_ORDER_001", "shipment_list")

    shipments = authenticated_client.shipment.list(params={
        'order_reference': 'VB_ORDER_001',
    })

    assert isinstance(shipments, list)

    assert len(shipments) == 1

    assert shipments[0]['id'] == '1701bf71-0b9a-4984-bee5-c9e83b7d2c1d'
    assert shipments[0]['order_reference'] == 'MW_ORD_001'
    assert shipments[0]['labels'][0]['tracking_code'] == 'ewh-pick-up'
    assert shipments[0]['labels'][0]['tracking_url'] == '#'
    assert shipments[0]['labels'][0]['shipping_method']['id'] == '7e808ac8-4167-11e9-92f0-0242ac140006'
    assert shipments[0]['labels'][0]['shipping_method']['name'] == 'eWarehousing afhaal order'


def test_get_shipment(authenticated_client, response):
    """Retrieve a single shipment by shipment ID."""
    response.get("https://api.ewarehousing.com/wms/orders/1701bf71-0b9a-4984-bee5-c9e83b7d2c1d", "shipment_single")

    shipment = authenticated_client.order.get('1701bf71-0b9a-4984-bee5-c9e83b7d2c1d')
    assert isinstance(shipment, dict)

    assert shipment['id'] == '1701bf71-0b9a-4984-bee5-c9e83b7d2c1d'
    assert shipment['order_reference'] == 'MW_ORD_001'
    assert shipment['labels'][0]['tracking_code'] == 'ewh-pick-up'
    assert shipment['labels'][0]['tracking_url'] == '#'
    assert shipment['labels'][0]['shipping_method']['id'] == '7e808ac8-4167-11e9-92f0-0242ac140006'
    assert shipment['labels'][0]['shipping_method']['name'] == 'eWarehousing afhaal order'

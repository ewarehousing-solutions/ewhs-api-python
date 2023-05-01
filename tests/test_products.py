def test_list_products(authenticated_client, response):
    """Retrieve a list of products"""
    response.get(f"https://api.ewarehousing.com/wms/articles/", "products_list")

    products = authenticated_client.product.list()

    assert isinstance(products, list)
    assert len(products) == 2
    assert products[0]['name'] == 'T-shirt'
    assert products[1]['name'] == 'Broek'


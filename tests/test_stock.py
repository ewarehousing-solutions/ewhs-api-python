def test_list_stock_levels(authenticated_client, response):
    """Retrieve a list of stock levels"""
    response.get(f"https://eu.middleware.ewarehousing-solutions.com/wms/stock/", "stock_list")

    stock = authenticated_client.stock.list()
    assert isinstance(stock, list)

    assert len(stock) == 4

    assert stock[0]['id'] == 'f2894c16-399e-4ca1-9151-489775a6519c'
    assert stock[0]['article_code'] == 'SHRT-R'
    assert stock[0]['ean'] == '8785073983111'
    assert stock[0]['stock_physical'] == 1
    assert stock[0]['stock_salable'] == 1
    assert stock[0]['stock_available'] == 0
    assert stock[0]['stock_quarantaine'] == 0
    assert stock[0]['stock_plannable'] == 0

    assert stock[1]['id'] == 'f2894c16-399e-4ca1-9151-489775a6519d'
    assert stock[1]['article_code'] == 'SNPBCK'
    assert stock[1]['stock_physical'] == 0

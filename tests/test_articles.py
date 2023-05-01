def test_list_articles(authenticated_client, response):
    """Retrieve a list of articles"""
    response.get(f"https://eu.middleware.ewarehousing-solutions.com/wms/articles/", "article_list")

    articles = authenticated_client.article.list()

    assert isinstance(articles, list)
    assert len(articles) == 2
    assert articles[0]['name'] == 'T-shirt'
    assert articles[1]['name'] == 'Broek'


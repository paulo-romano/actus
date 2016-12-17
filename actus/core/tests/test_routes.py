def test_must_redirect_to_login_page_if_not_loged(client):
    response = client.get('/')
    assert response.status_code == 302

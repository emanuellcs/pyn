def test_passphrase_generation(client):
    response = client.get('/passphrase/')
    assert response.status_code == 200
    assert b'Passphrase Generator' in response.data
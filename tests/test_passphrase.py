def test_passphrase_index(client):
    response = client.get("/passphrase/")
    assert response.status_code == 200
    assert b"Passphrase" in response.data


def test_passphrase_generation(client):
    response = client.post(
        "/passphrase/generate",
        data={"num_words": 4, "generator_type": "diceware", "separator": "-"},
        headers={"HX-Request": "true"},
    )
    assert response.status_code == 200
    assert b"Generated Password" in response.data

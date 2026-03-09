def test_password_index(client):
    response = client.get("/passwords/")
    assert response.status_code == 200
    assert b"Generate" in response.data


def test_password_generation(client):
    # Testing HTMX endpoint
    response = client.post(
        "/passwords/generate",
        data={
            "length": 12,
            "use_upper": "on",
            "use_lower": "on",
            "use_digits": "on",
            "use_special": "on",
        },
        headers={"HX-Request": "true"},
    )
    assert response.status_code == 200
    assert b"Generated Password" in response.data


def test_password_analysis_input(client):
    response = client.post(
        "/passwords/analyze_input", data={"password": "Str0ngP@ssw0rd!"}
    )
    assert response.status_code == 200
    assert b"Entropy" in response.data

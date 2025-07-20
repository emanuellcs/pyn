def test_password_analysis(client):
    response = client.post('/passwords/analyze', json={'passwords': 'password123'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'analysis_results' in json_data
    assert len(json_data['analysis_results']) > 0

def test_password_generation(client):
    response = client.post('/passwords/', json={
        'length': 12,
        'use_upper': True,
        'use_lower': True,
        'use_digits': True,
        'use_special': True
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'password_result' in json_data
    assert 'analysis' in json_data


def test_detailed_password_analysis(client):
    """
    Test the new detailed password analysis endpoint.
    """
    response = client.post('/passwords/analyze', json={'passwords': 'Str0ngP@ssw0rd!'})
    assert response.status_code == 200
    json_data = response.get_json()

    # Check top-level keys
    assert 'analysis_results' in json_data
    results = json_data['analysis_results'][0]
    assert 'strength' in results
    assert 'details' in results

    # Check strength
    assert results['strength'] in ["Weak", "Good", "Strong", "Very Strong"]

    # Check details structure
    details = results['details']
    assert isinstance(details, list)
    for item in details:
        assert 'title' in item
        assert 'explanation' in item

    # Check for specific details
    titles = [item['title'] for item in details]
    assert 'Length' in titles
    assert 'Character Variety' in titles
    assert 'Time to Crack (Offline, Fast Hashing)' in titles
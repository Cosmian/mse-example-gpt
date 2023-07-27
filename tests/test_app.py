import requests


def test_health(url, certificate):
    response = requests.get(f"{url}/health", verify=certificate)
    assert response.status_code == 200


def test_generate_get(url, certificate):
    response = requests.get(f"{url}/generate?prompt=SGVsbG8K", verify=certificate)
    assert response.status_code == 200


def test_generate_post(url, certificate):
    data = {"query": "Test"}
    response = requests.post(f"{url}/generate", json=data, verify=certificate)
    assert response.status_code == 200

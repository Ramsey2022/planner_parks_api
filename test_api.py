import json


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200


def test_root(client):
    res = client.get("/")
    assert res.json["message"] == "Server is running!"


def test_parks(client, postal_code):
    res = client.post(
        "/parks", data=json.dumps(postal_code), content_type="application/json"
    )
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"

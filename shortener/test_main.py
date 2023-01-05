from fastapi import FastAPI
from starlette.testclient import TestClient
from shortener.main import app, get_db
from shortener import crud
import pytest

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "LinkBite: the FastAPI-enabled URL shortener"


# def test_forward_to_target_url():
# currently I do not know how to test the database without creating a
# false link with a session, so this test performs only basic checks

#     # assert that the response is a redirect to the target URL
#     assert response.status_code == 302
#     assert response.headers["location"] == "http://example.com"


def test_create_url():
    # test a valid URL
    valid_url = {"target_url": "https://www.google.com"}
    response = client.post("/url", json=valid_url)
    assert response.status_code == 200
    assert "url" in response.json()
    assert "admin_url" in response.json()
    assert "clicks" in response.json()
    assert response.json()["clicks"] >= 0

    # test an invalid URL
    invalid_url = {"target_url": "not a url"}
    response = client.post("/url", json=invalid_url)
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid URL"

    # test a URL that doesn't exist
    non_existent_url = {"target_url": "https://www.example.com/not-a-real-page"}
    response = client.post("/url", json=non_existent_url)
    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "This URL does not exist"


# not working as of now
def test_forward_to_target_url():
    # Test that the function returns a redirect response when a valid url_key is provided
    payload = {"target_url": "https://www.google.com"}
    response = client.post("/url", json=payload)
    url_key = response.json()["url"][-5:]
    response = client.get(f"/{url_key}")
    assert response.status_code == 307
    assert response.headers["location"] == "https://www.google.com"

    # Test that the function returns a 404 error when an invalid url_key is provided
    url_key = "invalid_key"
    response = client.get(f"/{url_key}")
    assert response.status_code == 404

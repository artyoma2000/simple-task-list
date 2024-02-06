import pytest
import requests
import json


@pytest.fixture
def url():
    return "http://localhost:8080/tasks"


@pytest.fixture
def headers():
    return {"Content-Type": "application/json"}


@pytest.fixture
def data():
    return {
        "tasks": "Купить коня 5/0"
    }


@pytest.fixture
def json_data(data):
    return json.dumps(data)


def test_post(url, headers, json_data):
    response = requests.post(url, data=json_data, headers=headers)
    assert response.status_code == 200


def test_get(url, headers):
    response = requests.get(url, headers=headers)
    assert response.status_code == 200

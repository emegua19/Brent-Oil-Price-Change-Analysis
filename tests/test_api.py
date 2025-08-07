# tests/test_api.py

import pytest
import os
import sys

# Adjust path to import the Flask app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from backend.app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert "API is running" in data["message"]  # ✅ Updated to match your current message


def test_log_returns_endpoint(client):
    response = client.get("/log-returns")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    if data:
        assert "Date" in data[0]
        assert "LogReturn" in data[0]


def test_change_points_endpoint(client):
    response = client.get("/change-points")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    if data:
        assert "Date" in data[0]
        assert "Tau_Mode" in data[0]


def test_matched_events_endpoint(client):
    response = client.get("/matched-events")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    if data:
        assert "Change_Point_Date" in data[0]
        assert "Event_Description" in data[0]
        assert "Event_Date" in data[0]

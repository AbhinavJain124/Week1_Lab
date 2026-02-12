"""Pytest configuration and fixtures for testing the FastAPI app."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Store the original activities for resetting between tests
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Basketball": {
        "description": "Team sport focusing on basketball skills and games",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis techniques and participate in friendly matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
        "max_participants": 10,
        "participants": ["jessica@mergington.edu"]
    },
    "Painting Studio": {
        "description": "Explore painting techniques and create artwork",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["maya@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act in plays and develop theatrical skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["james@mergington.edu", "lucy@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and critical thinking skills",
        "schedule": "Mondays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 12,
        "participants": ["ryan@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["sarah@mergington.edu", "tyler@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to original state before each test."""
    activities.clear()
    activities.update({k: {"description": v["description"],
                          "schedule": v["schedule"],
                          "max_participants": v["max_participants"],
                          "participants": v["participants"].copy()}
                      for k, v in ORIGINAL_ACTIVITIES.items()})
    yield
    activities.clear()
    activities.update({k: {"description": v["description"],
                          "schedule": v["schedule"],
                          "max_participants": v["max_participants"],
                          "participants": v["participants"].copy()}
                      for k, v in ORIGINAL_ACTIVITIES.items()})

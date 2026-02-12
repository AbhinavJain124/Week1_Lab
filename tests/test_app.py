"""Tests for the Mergington High School Activities API."""

import pytest


class TestActivitiesAPI:
    """Test suite for the activities API endpoints."""

    def test_get_activities(self, client):
        """Test retrieving all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Basketball" in data
        assert len(data) == 9

    def test_get_activities_structure(self, client):
        """Test that activities have the correct structure."""
        response = client.get("/activities")
        data = response.json()
        
        activity = data["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

    def test_signup_success(self, client):
        """Test successful signup for an activity."""
        response = client.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]

    def test_signup_adds_participant(self, client):
        """Test that signup actually adds the participant to the activity."""
        # Verify initial state
        response = client.get("/activities")
        initial_participants = len(response.json()["Basketball"]["participants"])
        
        # Sign up
        client.post("/activities/Basketball/signup?email=newstudent@mergington.edu")
        
        # Verify participant was added
        response = client.get("/activities")
        updated_participants = response.json()["Basketball"]["participants"]
        assert len(updated_participants) == initial_participants + 1
        assert "newstudent@mergington.edu" in updated_participants

    def test_signup_duplicate_fails(self, client):
        """Test that signing up twice for the same activity fails."""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Try to sign up again with an email already registered
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 400
        
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_nonexistent_activity_fails(self, client):
        """Test that signup fails for a nonexistent activity."""
        response = client.post(
            "/activities/Nonexistent Club/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_signup_activity_full_fails(self, client, ):
        """Test that signup fails when activity is at capacity."""
        activity = "Tennis Club"
        
        # Fill the activity to capacity (max 10, currently has 1 participant)
        for i in range(9):
            email = f"student{i}@mergington.edu"
            response = client.post(f"/activities/{activity}/signup?email={email}")
            assert response.status_code == 200
        
        # Try to sign up when full
        response = client.post(
            f"/activities/{activity}/signup?email=overfull@mergington.edu"
        )
        assert response.status_code == 400
        assert "full" in response.json()["detail"]

    def test_unregister_success(self, client):
        """Test successful unregistration from an activity."""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_unregister_removes_participant(self, client):
        """Test that unregister actually removes the participant."""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Verify initial state
        response = client.get("/activities")
        initial_participants = response.json()[activity]["participants"]
        assert email in initial_participants
        
        # Unregister
        client.delete(f"/activities/{activity}/unregister?email={email}")
        
        # Verify participant was removed
        response = client.get("/activities")
        updated_participants = response.json()[activity]["participants"]
        assert email not in updated_participants
        assert len(updated_participants) == len(initial_participants) - 1

    def test_unregister_not_registered_fails(self, client):
        """Test that unregistering fails when student is not registered."""
        response = client.delete(
            "/activities/Basketball/unregister?email=notregistered@mergington.edu"
        )
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]

    def test_unregister_nonexistent_activity_fails(self, client):
        """Test that unregister fails for a nonexistent activity."""
        response = client.delete(
            "/activities/Nonexistent Club/unregister?email=student@mergington.edu"
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_signup_and_unregister_cycle(self, client):
        """Test the full cycle of signing up and unregistering."""
        email = "testcycle@mergington.edu"
        activity = "Gym Class"
        
        # Sign up
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
        
        # Verify participant was added
        response = client.get("/activities")
        assert email in response.json()[activity]["participants"]
        
        # Unregister
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        assert response.status_code == 200
        
        # Verify participant was removed
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]

    def test_multiple_signups_different_students(self, client):
        """Test that multiple students can sign up for the same activity."""
        activity = "Programming Class"
        
        emails = [f"student{i}@mergington.edu" for i in range(5)]
        
        for email in emails:
            response = client.post(f"/activities/{activity}/signup?email={email}")
            assert response.status_code == 200
        
        # Verify all were added
        response = client.get("/activities")
        participants = response.json()[activity]["participants"]
        
        for email in emails:
            assert email in participants

"""Tests for POST /activities/{activity_name}/signup endpoint"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


class TestSignupForActivity:
    """Test suite for signing up students for activities"""

    def test_signup_new_student_returns_200(self):
        """Test that a new student can successfully sign up for an activity"""
        # Arrange
        activity = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]

        # Verify student was added to participants
        activities_response = client.get("/activities")
        assert email in activities_response.json()[activity]["participants"]

    def test_signup_student_already_enrolled_returns_400(self):
        """Test that signing up an already-enrolled student returns 400"""
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"  # Already enrolled in Chess Club

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_to_nonexistent_activity_returns_404(self):
        """Test that signing up to a non-existent activity returns 404"""
        # Arrange
        activity = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_maintains_max_participants_limit_in_data(self):
        """Test that max_participants setting is maintained after signup"""
        # Arrange
        activity = "Programming Class"
        email = "another_student@mergington.edu"
        initial_response = client.get("/activities")
        initial_max = initial_response.json()[activity]["max_participants"]

        # Act
        client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        updated_response = client.get("/activities")
        updated_max = updated_response.json()[activity]["max_participants"]
        assert updated_max == initial_max  # Max should not change

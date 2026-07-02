"""Tests for DELETE /activities/{activity_name}/signup endpoint"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


class TestUnregisterFromActivity:
    """Test suite for unregistering students from activities"""

    def test_unregister_existing_participant_returns_200(self):
        """Test that an enrolled student can successfully unregister from an activity"""
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"  # Already enrolled
        initial_response = client.get("/activities")
        initial_participants = initial_response.json()[activity]["participants"].copy()

        # Act
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email in response.json()["message"]

        # Verify student was removed from participants
        updated_response = client.get("/activities")
        updated_participants = updated_response.json()[activity]["participants"]
        assert email not in updated_participants
        assert len(updated_participants) == len(initial_participants) - 1

    def test_unregister_non_enrolled_student_returns_400(self):
        """Test that unregistering a non-enrolled student returns 400"""
        # Arrange
        activity = "Soccer Team"
        email = "notenrolled@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_from_nonexistent_activity_returns_404(self):
        """Test that unregistering from a non-existent activity returns 404"""
        # Arrange
        activity = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_decreases_participant_count(self):
        """Test that unregistering properly decreases the participant count"""
        # Arrange
        activity = "Basketball Club"
        email = "liam@mergington.edu"  # Already enrolled
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity]["participants"])

        # Act
        client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity]["participants"])
        assert updated_count == initial_count - 1

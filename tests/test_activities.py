"""Tests for GET /activities endpoint"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


class TestGetActivities:
    """Test suite for retrieving all activities"""

    def test_get_all_activities_returns_200(self):
        """Test that GET /activities returns all activities with 200 status"""
        # Arrange
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Soccer Team",
            "Basketball Club", "Art Studio", "Drama Club", "Math Olympiad", "Science Club"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9
        for activity_name in expected_activities:
            assert activity_name in activities

    def test_get_activities_returns_correct_structure(self):
        """Test that activities have required fields"""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(activity_data.keys())
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)

    def test_get_activities_participants_are_populated(self):
        """Test that activities have initial participants"""
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_data in activities.values():
            assert len(activity_data["participants"]) > 0
            assert all(isinstance(email, str) for email in activity_data["participants"])

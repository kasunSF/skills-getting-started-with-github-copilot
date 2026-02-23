"""
Backend tests for High School Activity Management API

Uses AAA (Arrange-Act-Assert) pattern for clear test structure.
"""
import urllib.parse
from src.app import activities


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client):
        """
        Arrange: API is ready with initial activities
        Act: Make GET request to /activities
        Assert: Returns 200 and all activities are present
        """
        # Arrange (fixture handles setup)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Basketball Team" in data
        assert "Programming Class" in data
        assert len(data) == len(activities)
    
    def test_get_activities_includes_participant_details(self, client):
        """
        Arrange: Activities have participants data
        Act: Make GET request to /activities
        Assert: Response includes participant info for each activity
        """
        # Arrange (fixture handles setup)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        data = response.json()
        assert "participants" in data["Chess Club"]
        assert isinstance(data["Chess Club"]["participants"], list)
        assert len(data["Chess Club"]["participants"]) > 0


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success(self, client):
        """
        Arrange: New student email and existing activity
        Act: POST signup request with activity name and email
        Assert: Returns 200, success message, and participant added to list
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"
        encoded_name = urllib.parse.quote(activity_name, safe='')
        
        # Act
        response = client.post(
            f"/activities/{encoded_name}/signup",
            params={"email": new_email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}
        assert new_email in activities[activity_name]["participants"]
    
    def test_signup_duplicate_fails(self, client):
        """
        Arrange: Student already signed up for activity
        Act: POST signup request with existing participant email
        Assert: Returns 400 with duplicate error message
        """
        # Arrange
        activity_name = "Basketball Team"
        existing_email = "alex@mergington.edu"  # Already in initial data
        encoded_name = urllib.parse.quote(activity_name, safe='')
        
        # Act
        response = client.post(
            f"/activities/{encoded_name}/signup",
            params={"email": existing_email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json() == {"detail": "Student already signed up"}
    
    def test_signup_to_nonexistent_activity_fails(self, client):
        """
        Arrange: Activity does not exist
        Act: POST signup request to non-existent activity
        Assert: Returns 404 with not found error
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        encoded_name = urllib.parse.quote(activity_name, safe='')
        
        # Act
        response = client.post(
            f"/activities/{encoded_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json() == {"detail": "Activity not found"}


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/signup endpoint"""
    
    def test_unregister_success(self, client):
        """
        Arrange: Existing participant in activity
        Act: DELETE request to unregister participant
        Assert: Returns 200, success message, and participant removed from list
        """
        # Arrange
        activity_name = "Basketball Team"
        email = "alex@mergington.edu"
        encoded_name = urllib.parse.quote(activity_name, safe='')
        
        # Verify participant exists before deletion
        assert email in activities[activity_name]["participants"]
        
        # Act
        response = client.delete(
            f"/activities/{encoded_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
        assert email not in activities[activity_name]["participants"]
    
    def test_unregister_not_signed_up_fails(self, client):
        """
        Arrange: Student not signed up for activity
        Act: DELETE request to unregister non-participant
        Assert: Returns 400 with error message
        """
        # Arrange
        activity_name = "Tennis Club"
        email = "nobody@mergington.edu"  # Not in initial data
        encoded_name = urllib.parse.quote(activity_name, safe='')
        
        # Act
        response = client.delete(
            f"/activities/{encoded_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json() == {"detail": "Student not signed up"}
    
    def test_unregister_from_nonexistent_activity_fails(self, client):
        """
        Arrange: Activity does not exist
        Act: DELETE request from non-existent activity
        Assert: Returns 404 with not found error
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        encoded_name = urllib.parse.quote(activity_name, safe='')
        
        # Act
        response = client.delete(
            f"/activities/{encoded_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json() == {"detail": "Activity not found"}

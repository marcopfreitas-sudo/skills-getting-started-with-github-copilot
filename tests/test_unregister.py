def test_unregister_success_removes_participant(client):
    """Test that a registered student can successfully unregister from an activity"""
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity]["participants"]


def test_unregister_nonexistent_activity_returns_404(client):
    """Test that unregistering from a non-existent activity returns 404"""
    # Arrange
    activity = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_not_registered_returns_400(client):
    """Test that unregistering a student not in activity returns 400"""
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not registered for this activity"


def test_unregister_opens_spot_for_new_participant(client):
    """Test that unregistering a participant allows a new one to join full activity"""
    # Arrange
    activity = "Small Activity"  # max_participants = 1
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    # Act - first signup fills the activity
    response1 = client.post(f"/activities/{activity}/signup?email={email1}")
    assert response1.status_code == 200
    
    # Act - second signup fails (full)
    response2 = client.post(f"/activities/{activity}/signup?email={email2}")
    assert response2.status_code == 400
    
    # Act - unregister first student
    unregister_response = client.delete(f"/activities/{activity}/unregister?email={email1}")
    assert unregister_response.status_code == 200
    
    # Act - now second student should be able to sign up
    response3 = client.post(f"/activities/{activity}/signup?email={email2}")
    
    # Assert
    assert response3.status_code == 200
    activities_response = client.get("/activities")
    data = activities_response.json()
    assert email1 not in data[activity]["participants"]
    assert email2 in data[activity]["participants"]

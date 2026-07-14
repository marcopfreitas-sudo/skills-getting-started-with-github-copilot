def test_signup_success_adds_participant(client):
    """Test that a new student can successfully sign up for an activity"""
    # Arrange
    activity = "Small Activity"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    
    # Verify participant was added
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity]["participants"]


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signing up for a non-existent activity returns 404"""
    # Arrange
    activity = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_registration_returns_400(client):
    """Test that a student cannot sign up twice for the same activity"""
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_full_activity_returns_400(client):
    """Test that signup fails when activity reaches max capacity"""
    # Arrange
    activity = "Small Activity"  # max_participants = 1
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    # Act - first signup should succeed
    response1 = client.post(f"/activities/{activity}/signup?email={email1}")
    assert response1.status_code == 200
    
    # Act - second signup should fail (activity is now full)
    response2 = client.post(f"/activities/{activity}/signup?email={email2}")
    
    # Assert
    assert response2.status_code == 400
    assert "max capacity" in response2.json()["detail"].lower()


def test_signup_multiple_activities_same_student(client):
    """Test that a student can sign up for multiple different activities"""
    # Arrange
    student = "student@mergington.edu"
    activity1 = "Small Activity"
    activity2 = "Chess Club"
    
    # Act
    response1 = client.post(f"/activities/{activity1}/signup?email={student}")
    response2 = client.post(f"/activities/{activity2}/signup?email={student}")
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    activities_response = client.get("/activities")
    data = activities_response.json()
    assert student in data[activity1]["participants"]
    assert student in data[activity2]["participants"]

def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities"""
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Small Activity"]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all(name in data for name in expected_activities)


def test_get_activities_includes_required_fields(client):
    """Test that each activity has all required fields"""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    for activity in data.values():
        assert all(field in activity for field in required_fields)
        assert isinstance(activity["participants"], list)
        assert isinstance(activity["max_participants"], int)


def test_get_activities_returns_correct_participant_counts(client):
    """Test that activity response includes correct participant information"""
    # Arrange
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu"]
    assert len(data["Programming Class"]["participants"]) == 1
    assert len(data["Small Activity"]["participants"]) == 0

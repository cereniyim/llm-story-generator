from unittest.mock import patch

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@patch("src.gateway.MongoDBGateway.get_processed_activities")
def test_get_all_processed_activities_200(mock_get_processed_activities):
    activities = [
        {
            "time": 120,
            "elevation": 50.5,
            "speed": 60,
            "distance": 35,
            "story_title": "A sunny day run",
            "story_content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean et augue id nunc fermentum malesuada in sed sapien. Aliquam malesuada eu enim non convallis. Donec id sapien arcu.",
        },
        {
            "time": 500,
            "elevation": 50.5,
            "speed": 23,
            "distance": 43.9,
            "story_title": "A cloudy day jog",
            "story_content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean et augue id nunc fermentum malesuada in sed sapien. Aliquam malesuada eu enim non convallis. Donec id sapien arcu.",
        },
    ]
    mock_get_processed_activities.return_value = activities

    response = client.get("/activities/processed")
    result = response.json()

    assert response.status_code == 200
    assert result == activities


@patch("src.gateway.MongoDBGateway.get_processed_activities")
def test_get_all_processed_activities_404(mock_get_processed_activities):
    mock_get_processed_activities.return_value = []

    response = client.get("/activities/processed")
    assert response.status_code == 404
    assert response.json() == {"detail": "No processed activities"}

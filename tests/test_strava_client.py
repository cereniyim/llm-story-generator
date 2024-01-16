import pytest
import responses

from src.strava_client import (
    StravaClient,
    ActivityNotFoundError,
    ActivityBadRequestError,
    ClientAuthenticationError,
)


@pytest.mark.skip(reason="Integration test")
def test_authenticate():
    client = StravaClient()

    client.authenticate()

    assert StravaClient._access_token
    assert StravaClient._refresh_token
    assert not StravaClient._first_call


@pytest.mark.skip(reason="Integration test")
def test_refresh():
    client = StravaClient()
    StravaClient._refresh_token = "REPLACE ME"
    StravaClient._access_token = "REPLACE ME"

    client.refresh_token()

    assert StravaClient._access_token != "REPLACE ME"
    assert StravaClient._refresh_token != "REPLACE ME"


@pytest.mark.skip(reason="Integration test")
def test_get_activity():
    client = StravaClient()
    StravaClient._refresh_token = "REPLACE ME"
    StravaClient._access_token = "REPLACE ME"

    client.refresh_token()
    activity = client.get_activity(309525343)

    assert len(activity) > 0


@pytest.mark.skip(reason="Integration test")
def test_get_most_recent_activities():
    client = StravaClient()
    StravaClient._refresh_token = "REPLACE ME"
    StravaClient._access_token = "REPLACE ME"

    # StravaClient.refresh_token()
    activities = client.get_most_recent_activities()

    assert activities == [
        {
            "average_speed": 1.902,
            "distance": 117.9,
            "max_speed": 3.3,
            "moving_time": 62,
            "total_elevation_gain": 0.0,
        }
    ]


@pytest.fixture
def setup_data():
    activity_uri = "https://mock_uri/activity/"
    activity_id = "1234"
    return activity_uri, activity_id


@pytest.fixture
def setup_mock_success(setup_data):
    activity_uri, activity_id = setup_data

    mock_resp = {
        "average_speed": 25.0,
        "max_speed": 60.0,
        "distance": 100.0,
        "moving_time": 120,
        "total_elevation_gain": 200,
        "other_key": "other_value",
        "another_key": "another_value",
    }

    url = f"{activity_uri}{activity_id}?include_all_efforts=false"

    responses.add(responses.GET, url, json=mock_resp, status=200)
    return mock_resp


@responses.activate
def test_get_activity_200(setup_mock_success, setup_data):
    activity_uri, activity_id = setup_data
    client = StravaClient(activity_uri)
    client._access_token = "1234"

    result = client.get_activity(activity_id)

    assert result == {
        "average_speed": 25.0,
        "max_speed": 60.0,
        "distance": 100.0,
        "moving_time": 120,
        "total_elevation_gain": 200,
    }
    # drops unnecessary key, value pairs


@pytest.fixture
def setup_mock_not_found(setup_data):
    activity_uri, activity_id = setup_data

    url = f"{activity_uri}{activity_id}?include_all_efforts=false"

    responses.add(responses.GET, url, status=404)


@responses.activate
def test_get_activity_404(setup_data, setup_mock_not_found):
    activity_uri, activity_id = setup_data
    client = StravaClient(activity_uri)
    client._access_token = "1234"

    with pytest.raises(ActivityNotFoundError):
        _ = client.get_activity(activity_id)


@pytest.fixture
def setup_mock_bad_request(setup_data):
    activity_uri, activity_id = setup_data

    url = f"{activity_uri}{activity_id}?include_all_efforts=false"

    responses.add(responses.GET, url, status=400)


@responses.activate
def test_get_activity_400(setup_data, setup_mock_bad_request):
    activity_uri, activity_id = setup_data
    client = StravaClient(activity_uri)
    client._access_token = "1234"

    with pytest.raises(ActivityBadRequestError):
        _ = client.get_activity(activity_id)


@pytest.fixture
def setup_mock_authentication_failed(setup_data):
    activity_uri, activity_id = setup_data

    url = f"{activity_uri}{activity_id}?include_all_efforts=false"

    responses.add(responses.GET, url, status=401)


@responses.activate
def test_get_activity_401(setup_data, setup_mock_authentication_failed):
    activity_uri, activity_id = setup_data
    client = StravaClient(activity_uri)
    client._access_token = "1234"

    with pytest.raises(ClientAuthenticationError):
        _ = client.get_activity(activity_id)

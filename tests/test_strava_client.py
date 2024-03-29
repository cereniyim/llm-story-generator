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
def test_refresh_token():
    client = StravaClient()

    client.refresh_token()

    assert StravaClient._access_token is not None


@pytest.mark.skip(reason="Integration test")
def test_get_activity():
    client = StravaClient()

    client.refresh_token()
    activity = client.get_activity(309525343)

    assert activity == {
        "activity_id": 309525343,
        "distance": 117.9,
        "elevation": 0.0,
        "speed": 3.3,
        "time": 62,
    }


@pytest.mark.skip(reason="Integration test")
def test_get_most_recent_activities():
    client = StravaClient()
    client.refresh_token()

    activities = client.get_most_recent_activities()

    assert activities == [
        {
            "activity_id": 309525343,
            "distance": 117.9,
            "speed": 3.3,
            "time": 62,
            "elevation": 0.0,
        }
    ]


@pytest.fixture
def setup_data():
    activity_uri = "https://mock_uri/activity/"
    activity_id = 1234
    return activity_uri, activity_id


@pytest.fixture
def setup_mock_success(setup_data):
    activity_uri, activity_id = setup_data

    mock_resp = {
        "activity_id": activity_id,
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
        "activity_id": activity_id,
        "speed": 60.0,
        "distance": 100.0,
        "time": 120,
        "elevation": 200,
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

import pytest

from src.gateway import MongoDBGateway, NoResultFound
from src.generators import Story


pytestmark = pytest.mark.skip(reason="requires MongoDB running locally")
# TODO implement unit tests by mocking MongoDBGateway current tests requires MongoDB up and running locally
# TODO make tests independent


@pytest.fixture(scope="module")
def gateway():
    return MongoDBGateway(
        uri="mongodb://localhost:27017",
        db_name="activities",
        collection_name="activity_collection",
    )


def test_bulk_save(gateway):
    activities = [
        {"activity_id": 1},
        {"activity_id": 2},
        {
            "activity_id": 3,
            "story_title": "title",
            "story_content": "a story with multiple words",
        },
        {
            "activity_id": 4,
            "story_title": "Another title",
            "story_content": "another story with multiple words",
        },
    ]
    gateway.bulk_save(activities)

    for idx, activity in enumerate(activities):
        activity.pop("_id")
        assert gateway.get(idx + 1) == activity


def test_get_processed_activities(gateway):
    res = gateway.get_processed_activities()

    assert len(res) == 2
    assert res[0] == {
        "activity_id": 3,
        "story_title": "title",
        "story_content": "a story with multiple words",
    }
    assert res[1] == {
        "activity_id": 4,
        "story_title": "Another title",
        "story_content": "another story with multiple words",
    }


def test_get_success(gateway):
    assert gateway.get(1) == {"activity_id": 1}


def test_update(gateway):
    activity = {"activity_id": 1}
    story = Story("title", "story content")
    gateway.update(activity, story.__dict__)

    activity.update(story.__dict__)
    assert gateway.get(1) == activity


def test_save_one(gateway):
    activity = {"activity_id": 47}
    gateway.save_one(activity)

    assert gateway.get(47) == {"activity_id": 47}


def test_get_fails(gateway):
    with pytest.raises(NoResultFound):
        gateway.get(1000)

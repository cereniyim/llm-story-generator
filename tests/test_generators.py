from src.generators import StoryGenerator


def test_generate_story():
    activity = {
        "activity_id": 1,
        "speed": 60.0,
        "distance": 100.0,
        "time": 120,
        "elevation": 200,
    }
    story_generator = StoryGenerator()
    res = story_generator.generate(activity)

    assert len(res.story_title) > 0
    for key, value in activity.items():
        if key != "activity_id":
            assert str(int(value)) in res.story_content

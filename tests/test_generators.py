from src.generators import StoryGenerator


def test_generate_story():
    activity_metrics = {
        "speed": 60.0,
        "distance": 100.0,
        "time": 120,
        "elevation": 200,
    }
    story_generator = StoryGenerator()
    res = story_generator.generate(activity_metrics)

    assert len(res.title) > 0
    for value in activity_metrics.values():
        assert str(int(value)) in res.content

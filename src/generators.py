from dataclasses import dataclass


@dataclass
class Story:
    title: str
    content: str


class StoryGenerator:
    def __init__(self):
        # used pre-trained model as attribute
        pass

    def generate_story(self, activity: dict) -> Story:
        """
        Generates a title and a 50 word story for the given input with a Langchain model
        Parameters
        ----------
        speed
        distance
        moving_time
        elevation_gain

        Returns
        -------

        """
        pass


class ImageGenerator:
    # TODO
    pass

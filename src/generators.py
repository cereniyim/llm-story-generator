from dataclasses import dataclass

from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()


@dataclass
class Story:
    story_title: str
    story_content: str


class StoryGenerator:
    def __init__(self):
        self._llm_model = HuggingFaceHub(
            repo_id="openchat/openchat-3.5-0106",
        )
        self._story_prompt_template: PromptTemplate = PromptTemplate(
            input_variables=["metrics"],
            template="Write a 2 sentence story. First sentence must include these phrases: {metrics}. "
            "Second sentence will define nature. Provide a Title at the beginning.",
        )

    def generate(self, activity: dict) -> Story:
        """
        Generates story around 50 words and a title with https://huggingface.co/openchat/openchat-3.5-0106
        model with the given activity metrics

        Parameters
        ----------
        activity : dict
            A dictionary containing activity. Expected keys:
            - `activity_id`
            - `speed`
            - `distance`
            - `time`
            - `elevation`

        Returns
        -------
        Story
            A `Story` object with
            - `story_title`
            - `story_content`

        """
        story_llm_chain = LLMChain(
            prompt=self._story_prompt_template, llm=self._llm_model, verbose=False
        )
        metrics = activity.copy()
        metrics.pop("activity_id")
        prompt_metrics = ", ".join(f"{key} {value}" for key, value in metrics.items())
        story = story_llm_chain.run(prompt_metrics)
        title, content = story.split("\n\n")[2:4]
        return Story(story_title=title, story_content=content)


class ImageGenerator:
    # TODO
    pass

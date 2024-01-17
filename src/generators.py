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
            template="Write me a sentence, including these phrases: {metrics}. "
            "Then add 2 more sentences to make it a story. Provide a Title at the beginning.",
        )
        # TODO figure out why sentence is abruptly finishing

    def generate(self, activity: dict) -> Story:
        """
        Generates story and a title with https://huggingface.co/openchat/openchat-3.5-0106 model with the
        given activity metrics

        Parameters
        ----------
        activity : dict
            A dictionary containing the metrics of the activity. Expected keys:
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
        title = story.split("Title: ")[1].split("\n")[0]
        content = story.replace(f"\n\nTitle: {title}\n\n", "")
        return Story(story_title=title, story_content=content)


class ImageGenerator:
    # TODO
    pass

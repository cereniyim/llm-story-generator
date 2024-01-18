from abc import abstractmethod, ABC
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
    # story_image_link: Optional[str] = None


class AIGenerator(ABC):
    @abstractmethod
    def generate(self, input_: dict) -> Story:
        pass


class AIStoryGenerator(AIGenerator):
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
        title = story.split("Title: ")[1].split("\n")[0]
        # Title always comes after "Title: "
        content = sorted(story.split("\n\n"), key=lambda x: len(x), reverse=True)[0]
        # LLM might continue to generate the story resulting in abruptly finishing sentences
        # Get the logical text from the longest paragraph to have a meaningful story to read
        return Story(story_title=title, story_content=content)


class AIImageGenerator(AIGenerator):
    def __init__(self):
        # self._model: a text-to-image model
        # self._image_uploader: a s3 client that uploads generated images to s3 buckets using boto3
        pass

    def generate(self, story: dict) -> Story:
        """
        Generates image based on the story content and title provided

        Parameters
        ----------
        story: dictionary with following keys
            - story_title
            - story_content

        Returns
        -------
        Story object with the image link added

        """
        # generate image with self._model.run() or predict or any inference method
        # save generated image into temp directory
        # make sure image size is reasonable so include that in prompt
        # assign unique name to image file, UUID can be used
        # upload image to s3 bucket self._image_uploader.upload(filename)
        # delete the image file from temp directory
        # return s3 URL of the uploaded image
        raise NotImplementedError

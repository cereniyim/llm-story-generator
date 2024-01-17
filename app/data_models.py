from pydantic import BaseModel


class ProcessedActivity(BaseModel):
    speed: float
    distance: float
    elevation: float
    time: float
    story_title: str
    story_content: str

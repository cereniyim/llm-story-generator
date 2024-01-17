from pydantic import BaseModel


class ProcessedActivity(BaseModel):
    activity_id: int
    speed: float
    distance: float
    elevation: float
    time: float
    story_title: str
    story_content: str

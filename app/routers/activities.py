from fastapi import APIRouter, HTTPException

from app.data_models import ProcessedActivity
from src.gateway import MongoDBGateway
from src.strava_client import StravaClient, ClientAuthenticationError

router = APIRouter(
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal Server Error"},
    }
)
gateway = MongoDBGateway(
    uri="mongodb://localhost:27017",
    db_name="activities",
    collection_name="activity_collection",
)
strava_client = StravaClient()
StravaClient.refresh_token()


@router.get("/processed/")
def get_all_processed_activities() -> list[ProcessedActivity]:
    # Serve one API endpoint to list all the activities the system has ever processed
    all_activities = gateway.get_processed_activities()
    if not all_activities:
        raise HTTPException(status_code=404, detail="No processed activities")
    return [ProcessedActivity(**activity) for activity in all_activities]


@router.post("/", status_code=201, response_model=dict)
def save_recent_strava_activities():
    # gets last 3 activities from Strava saves them to DB
    try:
        activities = strava_client.get_most_recent_activities()
    except ClientAuthenticationError:
        StravaClient.refresh_token()
        activities = strava_client.get_most_recent_activities()
    if activities:
        gateway.bulk_save(activities)
        return {"message": f"Successfully saved {len(activities)} activities."}
    else:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error when getting activities from Strava",
        )


@router.put("/{activity_id}/")
def update_activity_with_story(activity_id: int) -> ProcessedActivity:
    # Serve one API endpoint that takes activity id as a parameter and returns the activity details, generated title and story
    # if activity not in DB get it from StravaClient
    # MongoDBGateway()
    #   try:
    #       activity: dict = MongoDBGateway.get(activity_id)
    #   except NoResultFound:
    #       activity = StravaClient(activity_id)
    # Generator initialization with proper prompts
    # story = Generator().generate_story(activity)
    # activity.update(story.as_dict)
    # updated_activity = MongoDBGateway.update(activity)
    # return updated_activity
    pass

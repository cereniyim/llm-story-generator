from fastapi import APIRouter

router = APIRouter()


@router.get("/processed/")
def get_all_processed_activities():
    # Serve one API endpoint to list all the activities the system has ever processed
    # gets processed activities from MongoDB
    # MongoDBGateway()
    # all_activities = MongoDBGateway.get_processed_activities()
    # return all_activities
    pass


@router.post("/")
def save_recent_strava_activities():
    # gets last 3 activities from Strava saves them to DB
    # activities = StravaClient().get_most_recent_activities()
    # MongoDBGateway.bulk_save(activities)
    pass


@router.put("/{activity_id}/")
def update_activity_with_story():
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

class StravaClient:
    def __init__(self):
        pass

    def authenticate(self):
        """
        Authenticates the user using Strava authentication logic
        Returns
        -------

        """
        pass

    def get_most_recent_activities(self, num_recent_activities=3) -> list[dict]:
        """
        Gets last 3 activities of the user from using Strava API
        returns it to the user

        Strava API does not offer any metadata so  I have to query until I get an empty list to get last 3
        activities of a user

        uses https://www.strava.com/api/v3/athlete/activities?page={page_number}&per_page=3

        Returns
        -------

        """
        pass

    def get_activity(self, activity_id) -> dict:
        """
        Gets the activity from the  StravaAPI
        Parameters
        ----------
        activity_id

        Returns
        -------

        """
        pass

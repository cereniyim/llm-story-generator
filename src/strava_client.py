from dotenv import load_dotenv
import os
import requests
from requests import Response, HTTPError

load_dotenv()


class ActivityNotFoundError(Exception):
    pass


class ClientAuthenticationError(Exception):
    pass


class ActivityBadRequestError(Exception):
    pass


class StravaClient:
    _access_token_uri = "https://www.strava.com/oauth/token"
    _token_type = "Bearer"
    _refresh_token = os.environ.get("STRAVA_REFRESH_TOKEN")
    _access_token = None
    _first_call = True

    def __init__(self, activity_uri: str = "https://www.strava.com/api/v3/activities/"):
        self._activity_uri = activity_uri

    @classmethod
    def authenticate(cls):
        """
        Authenticate the user with the Strava API. Only called for the first use with authorization code

        Note:
            This method requires environment variables:
                - STRAVA_CLIENT_ID: The client ID for your Strava application
                - STRAVA_CLIENT_SECRET: The client secret for your Strava application
                - STRAVA_AUTHORIZATION_CODE: Code obtained through redirected web uri

        More details available at: https://developers.strava.com/docs/getting-started/#account

        """
        # authorization code is in
        # "http://www.strava.com/oauth/authorize?client_id=<CLIENT_ID>&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all"
        # TODO this can also be achieved through auth0 package Management SDK https://pypi.org/project/auth0-python/
        payload = {
            "client_id": os.getenv("STRAVA_CLIENT_ID"),
            "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
            "code": os.getenv("STRAVA_AUTHORIZATION_CODE"),
        }
        response = requests.post(cls._access_token_uri, data=payload)
        data = response.json()
        cls._access_token = data["access_token"]
        cls._refresh_token = data["refresh_token"]
        cls._first_call = False
        print("Authentication successful")

    @classmethod
    def refresh_token(cls):
        """
        This method refreshes the access token for the Strava API.

        Note:
            This method requires environment variables:
                - STRAVA_CLIENT_ID: The client ID for your Strava application
                - STRAVA_CLIENT_SECRET: The client secret for your Strava application
                - STRAVA_REFRESH_TOKEN: The refresh token for your Strava application

        """
        payload = {
            "client_id": os.getenv("STRAVA_CLIENT_ID"),
            "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
            "refresh_token": cls._refresh_token,
            "grant_type": "refresh_token",
        }
        response = requests.post(cls._access_token_uri, data=payload)
        data = response.json()
        cls._access_token = data["access_token"]
        cls._refresh_token = data["refresh_token"]
        print("Refreshed access token")

    def get_most_recent_activities(self, num_recent_activities=3) -> list[dict]:
        """
        Gets most recent activities from Strava API. Assumes activities are sorted by date. It queries all the pages
        until Strava API does not provide any data, because there is no metadata returned about pagination. Returns
        parsed activities with only certain keys.

        Parameters
        ----------
        num_recent_activities: int
            default is 3

        Returns
        -------
        parsed_activities: list[dict]
            activities that have the following keys:
            - activity_id
            - distance
            - speed
            - time
            - elevation

        """
        activities = []
        page_number = 1
        while True:
            uri = f"{self._activity_uri}?page={page_number}"
            header = {"Authorization": f"{self._token_type} {self._access_token}"}
            response = requests.get(uri, headers=header)
            self._handle_errors(response)
            data = response.json()
            if len(data) == 0:
                break
            activities.extend(data)
            page_number += 1
        most_recent_activities = activities[-1 * num_recent_activities :]
        parsed_activities = [
            self._parse_response(activity) for activity in most_recent_activities
        ]
        return parsed_activities

    def get_activity(self, activity_id) -> dict:
        """
        Gets activity from Strava API given an activity_id. Returns parsed activities with only certain keys.

        Parameters
        ----------
        activity_id : int
            The ID of the activity to retrieve.

        Returns
        -------
        result: dict
            A dictionary containing the information related to the retrieved activity with following keys:
            - activity_id
            - distance
            - speed
            - time
            - elevation

        """
        header = {"Authorization": f"{self._token_type} {self._access_token}"}
        response = requests.get(
            f"{self._activity_uri}{activity_id}?include_all_efforts=false",
            headers=header,
        )
        self._handle_errors(response)
        data = response.json()
        data.update({"id": activity_id})
        result = self._parse_response(data)
        return result

    @staticmethod
    def _parse_response(raw_response: dict) -> dict:
        return {
            "activity_id": raw_response["id"],
            "speed": raw_response["max_speed"],
            "distance": raw_response["distance"],
            "time": raw_response["moving_time"],
            "elevation": raw_response["total_elevation_gain"],
        }

    @staticmethod
    def _handle_errors(response: Response):
        try:
            response.raise_for_status()
        except HTTPError:
            if response.status_code == 404:
                raise ActivityNotFoundError(f"Activity not found on Strava.")
            elif response.status_code == 400:
                raise ActivityBadRequestError(response.text)
            elif response.status_code == 401:
                raise ClientAuthenticationError("Authentication has failed.")

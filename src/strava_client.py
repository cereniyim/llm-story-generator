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
    _access_token = None
    _refresh_token = None
    _first_call = True

    def __init__(self, activity_uri: str = "https://www.strava.com/api/v3/activities/"):
        # self._authorization_uri = "https://www.strava.com/oauth/authorize"
        self._activity_uri = activity_uri
        # developers.strava.com

    @classmethod
    def authenticate(cls):
        """
        Authenticates the user for the first time with the code provided from Strava Web UI

        Returns
        -------

        """
        # authorization code is in
        # "http://www.strava.com/oauth/authorize?client_id=119923&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all"
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
        payload = {
            "client_id": os.getenv("STRAVA_CLIENT_ID"),
            "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
            "refresh_token": cls._refresh_token,
            "grant_type": "re fresh_token",
            "f": "json",
        }
        response = requests.post(cls._access_token_uri, data=payload)
        data = response.json()
        cls._access_token = data["access_token"]
        cls._refresh_token = data["refresh_token"]
        print("Refreshed access token")

    def get_most_recent_activities(self, num_recent_activities=3) -> list[dict]:
        """
        Gets last 3 activities of the user from using Strava API
        returns it to the user

        Strava API does not offer any metadata so  I have to query until I get an empty list to get last 3
        activities of a user

        uses https://www.strava.com/api/v3/athlete/activities?page={page_number}&per_page=3
        # Assumes activities are sorted

        Returns
        -------

        """
        header = {"Authorization": f"{self._token_type} {self._access_token}"}
        activities = []
        page_number = 1
        while True:
            uri = f"{self._activity_uri}?page={page_number}"
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
        Gets the activity from the  StravaAPI
        Parameters
        ----------
        activity_id

        Returns
        -------

        """
        header = {"Authorization": f"{self._token_type} {self._access_token}"}
        response = requests.get(
            f"{self._activity_uri}{activity_id}?include_all_efforts=false",
            headers=header,
        )
        self._handle_errors(response)
        result = self._parse_response(response.json())
        return result

    @staticmethod
    def _parse_response(raw_response: dict) -> dict:
        return {
            "average_speed": raw_response["average_speed"],
            "max_speed": raw_response["max_speed"],
            "distance": raw_response["distance"],
            "moving_time": raw_response["moving_time"],
            "total_elevation_gain": raw_response["total_elevation_gain"],
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

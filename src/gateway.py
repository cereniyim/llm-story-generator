from typing import Optional

from pymongo import MongoClient


class NoReultFound(BaseException):
    pass


class MongoDBGateway:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self._client = MongoClient(uri)
        self._db = self._client[db_name]
        self._collection = self._db[collection_name]

    def get(self, activity_id: Optional[int] = None) -> list[dict]:
        """
        returns the activity for the given activity id
        if activity not in DB returns NoResultFound

        Parameters
        ----------
        activity_id

        Returns
        -------

        """
        pass

    def update(self, activity_id: int) -> dict:
        """
        Updates activity inplace and adds title and story fields to MongoDB

        Parameters
        ----------
        activity_id

        Returns
        -------

        """
        pass

    def bulk_save(self, activities: list[dict]) -> None:
        """
        Saves list of activities to MongoDB

        Parameters
        ----------
        activities

        Returns
        -------

        """
        pass

    def get_processed_activities(self) -> list[dict]:
        """
        Gets activities from MongoDB who has
        - story
        - title

        fields
        Returns
        -------

        """

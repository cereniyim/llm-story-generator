from pymongo import MongoClient


class NoResultFound(BaseException):
    pass


class MongoDBGateway:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self._client = MongoClient(uri)
        self._db = self._client[db_name]
        self._collection = self._db[collection_name]

    def get(self, activity_id: int) -> dict:
        """
        Retrieve the document from the collection with the given activity ID.

        Parameters
        ----------
        activity_id : int
            The activity ID of the document to retrieve.

        Returns
        -------
        dict
            The retrieved document, excluding the "_id" field.

        Raises
        ------
        NoResultFound
            If no document with the specified activity ID is found in the collection.

        """
        result = self._collection.find_one({"activity_id": activity_id}, {"_id": 0})
        if result is None:
            raise NoResultFound(f"Activity {activity_id} not found")
        return result

    def update(self, activity_id: int, title: str, content: str) -> dict:
        """
        Update activity with the given title and content

        Parameters
        ----------
        activity_id : int
            The ID of the activity to be updated.
        title : str
            The new title to be assigned to the activity.
        content : str
            The new content to be assigned to the activity.

        Returns
        -------
        dict
            A dictionary representing the updated activity with the following keys:

        """
        self._collection.update_one(
            {"activity_id": activity_id},
            {"$set": {"story_title": title, "story_content": content}},
        )
        return {
            "activity_id": activity_id,
            "story_title": title,
            "story_content": content,
        }

    def bulk_save(self, activities: list[dict]) -> None:
        """
        This method bulk saves activities by inserting multiple documents into the specified collection.

        Parameters
        ----------
        activities : list[dict]
            A list containing dictionaries representing the activities to be saved. Each dictionary represents an activity.

        Returns
        -------
        None

        """
        self._collection.insert_many(activities)

    def get_processed_activities(self) -> list[dict]:
        """
        Retrieves a list of processed activities from the collection.

        Processed activity is an activity that has `story_title` and `story_content` attributes.

        Returns:
            list[dict]: A list of dictionaries representing the processed activities.

        """
        return list(
            self._collection.find(
                {
                    "$and": [
                        {"story_content": {"$exists": True}},
                        {"story_title": {"$exists": True}},
                    ]
                },
                {"_id": 0},
            )
        )

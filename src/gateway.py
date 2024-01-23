from pymongo import MongoClient


class NoResultFound(Exception):
    pass


class MongoDBGateway:
    _instance = None

    def __init__(self, uri: str, db_name: str, collection_name: str):
        self._client = MongoClient(uri)
        self._db = self._client[db_name]
        self._collection = self._db[collection_name]

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls(
                uri="mongodb://localhost:27017",
                db_name="activities",
                collection_name="activity_collection",
            )
        return cls._instance

    def get(self, document_id: int) -> dict:
        """
        Retrieve the document from the collection with the given activity ID.

        Parameters
        ----------
        document_id : int
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
        result = self._collection.find_one({"activity_id": document_id}, {"_id": 0})
        if result is None:
            raise NoResultFound(f"Activity {document_id} not found")
        return result

    def save_one(self, document: dict) -> None:
        """
        Saves the document to MongoDB

        Parameters
        ----------
        document : dict
            The document to be saved in the collection.

        Returns
        -------
        None

        """
        self._collection.insert_one(document.copy())

    def update(self, document: dict, update_dict: dict) -> dict:
        """
        Update document with the given update dictionary

        Parameters
        ----------
        document : dict
            The activity to be updated.
        update_dict: dict
            Key, value pairs that will be used to update the activity

        Returns
        -------
        dict
            A dictionary representing the updated activity with the new keys

        """
        self._collection.update_one(
            {"activity_id": document["activity_id"]},
            {"$set": update_dict},
        )
        document.update(update_dict)
        return document

    def bulk_save(self, documents: list[dict]) -> None:
        """
        This method bulk saves activities by inserting multiple documents into the specified collection.

        Parameters
        ----------
        documents : list[dict]
            A list containing dictionaries representing the activities to be saved. Each dictionary represents an activity.

        Returns
        -------
        None

        """
        self._collection.insert_many(documents)

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

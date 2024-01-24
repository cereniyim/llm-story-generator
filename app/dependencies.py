from src.gateway import MongoDBGateway


def get_db_gateway():
    return MongoDBGateway.get_instance()

from functools import lru_cache

from app.core.connectors.mongo import MongoConnector


@lru_cache(maxsize=16)
def get_mongo_client():
    return MongoConnector().get_connector()

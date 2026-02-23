from typing import Any

from loguru import logger
from pymongo import MongoClient

from app.core.settings import settings

from .base import BaseConnector


class MongoConnector(BaseConnector):
    def init_connector(self) -> Any:
        client = MongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=2000)

        logger.info("Mongo service initialized")
        return client

    def close_connector(self, connector_instance: MongoClient):
        connector_instance.close()
        logger.info("Mongo service closed")

    def get_connector(self) -> MongoClient:
        return super().get_connector()

from abc import ABC, abstractmethod
from typing import Any


class BaseConnector(ABC):
    _instance: Any = None
    _decorated_connector: Any

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BaseConnector, cls).__new__(cls, *args, **kwargs)
            cls._instance._decorated_connector = None
        return cls._instance

    def init(self):
        self._decorated_connector = self.init_connector()

    def close(self):
        self.close_connector(self._decorated_connector)
        self._decorated_connector = None

    def get_connector(self) -> Any:
        """Returns the connector if the connection is opened"""
        if not self._decorated_connector:
            raise ConnectionError("Connector is not initialized")
        return self._decorated_connector

    @abstractmethod
    def init_connector(self) -> Any:
        """Open the connection and return the connection instance"""
        ...

    @abstractmethod
    def close_connector(self, connector_instance: Any):
        """Close the connection"""
        ...

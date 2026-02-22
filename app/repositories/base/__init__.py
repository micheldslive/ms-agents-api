from abc import ABCMeta, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar

from app.entities.base import EntityBase

EntityClass = TypeVar("EntityClass", bound=EntityBase)


class BaseRepository(Generic[EntityClass], metaclass=ABCMeta):
    """Base repository interface."""

    @abstractmethod
    def create(self, data: dict[str, Any]) -> EntityClass: ...

    @abstractmethod
    def update(self, object_id: str, data: dict[str, Any]) -> EntityClass: ...

    @abstractmethod
    def retrieve(self, object_id: str) -> EntityClass: ...

    @abstractmethod
    def list(
        self,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        filters: Optional[dict[str, Any]] = None,
    ) -> list[EntityClass]: ...

    @abstractmethod
    def count(self, filters: Optional[dict[str, Any]] = None) -> int: ...

    @abstractmethod
    def delete(self, object_id: str): ...

    @abstractmethod
    def delete_many(self, filters: Optional[dict[str, Any]] = None) -> Any: ...

    @abstractmethod
    def group_by_field(
        self,
        group_field: str,
        value_field: str,
        filters: Optional[dict[str, Any]] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        sort_by: Optional[str] = None,
    ) -> List[dict[str, Any]]: ...


# Custom exception for document not found
class DocumentNotFoundError(Exception):
    pass

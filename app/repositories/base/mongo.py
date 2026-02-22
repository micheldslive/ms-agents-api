from typing import Any, List, Optional, Type

from bson import ObjectId
from pymongo.collection import Collection

from app.repositories.base import BaseRepository, DocumentNotFoundError, EntityClass
from app.utils.datetime import get_brazil_current_datetime


class MongoRepository(BaseRepository[EntityClass]):
    collection: Collection
    entity_cls: Type[EntityClass]

    def __init__(self, collection: Collection, entity_cls: Type[EntityClass]):
        self.collection = collection
        self.entity_cls = entity_cls

    def create(self, data: dict[str, Any]) -> EntityClass:
        data["created_at"] = get_brazil_current_datetime()
        # data["updated_at"] = get_brazil_current_datetime()

        inserted_id = self.collection.insert_one(document=data).inserted_id
        data = self.collection.find_one(filter={"_id": inserted_id})  # type: ignore

        data["_id"] = str(data["_id"])
        return self.entity_cls(**data)

    def update(self, object_id: str, data: dict[str, Any]) -> EntityClass:
        self.collection.update_one({"_id": ObjectId(object_id)}, {"$set": data})
        return self.retrieve(object_id)

    def retrieve(self, object_id: str) -> EntityClass:
        document = self.collection.find_one({"_id": ObjectId(object_id)})
        if document:
            return self.entity_cls(**document)
        raise DocumentNotFoundError(f"Document with id {object_id} not found")

    def list(
        self,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        filters: Optional[dict[str, Any]] = None,
        last_iterations: Optional[int] = None,
        order_by: Optional[str] = None,
        order_dir: Optional[int] = 1,
    ) -> list[EntityClass]:
        query = {}

        if filters:
            query.update(filters)

        cursor = self.collection.find(query)

        if order_by:
            cursor.sort(order_by, order_dir)

        if last_iterations:
            cursor.sort("created_at", -1).limit(last_iterations)
        else:
            if limit:
                cursor.limit(limit)
            if skip:
                cursor.skip(skip)

        data = list(cursor)
        data = [self.entity_cls(**d) for d in data]
        return data

    def count(self, filters: Optional[dict[str, Any]] = None) -> int:
        query = {}
        if filters:
            query.update(filters)
        return self.collection.count_documents(query)

    def delete(self, object_id: str):
        self.collection.delete_one({"_id": ObjectId(object_id)})

    def delete_many(
        self,
        filters: Optional[dict[str, Any]] = None,
    ):

        if filters:
            return self.collection.delete_many(filter=filters)
        return None

    def group_by_field(
        self,
        group_field: str,
        value_field: str,
        filters: Optional[dict[str, Any]] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        sort_by: Optional[str] = None,
    ) -> List[dict]:
        pipeline = []

        # Filtro opcional
        if filters:
            pipeline.append({"$match": filters})

        # Agrupamento
        pipeline.append(
            {
                "$group": {
                    "_id": f"${group_field}",
                    "values": {"$addToSet": f"${value_field}"},
                }
            }
        )

        # Projeção
        pipeline.append({"$project": {group_field: "$_id", "values": 1, "_id": 0}})

        # Ordenação opcional
        if sort_by:
            pipeline.append({"$sort": {sort_by: 1}})

        # Paginação
        if skip:
            pipeline.append({"$skip": skip})
        if limit:
            pipeline.append({"$limit": limit})

        return list(self.collection.aggregate(pipeline))

    def retrieve_by_filters(self, filters: dict[str, Any]) -> EntityClass:
        document = self.collection.find_one(filters)
        if document:
            return self.entity_cls(**document)
        raise DocumentNotFoundError(f"Document with filters {filters} not found")

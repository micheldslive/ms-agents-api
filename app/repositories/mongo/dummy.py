from pymongo.collection import Collection

from app.entities.dummy import DummyEntity
from app.repositories.base.mongo import MongoRepository


class DummyMongoRepository(MongoRepository[DummyEntity]):
    def __init__(self, collection: Collection):
        super().__init__(collection, entity_cls=DummyEntity)

from pymongo.collection import Collection

from app.entities.tools import ToolsEntity
from app.repositories.base.mongo import MongoRepository


class ToolsMongoRepository(MongoRepository[ToolsEntity]):
    def __init__(self, collection: Collection):
        super().__init__(collection, entity_cls=ToolsEntity)

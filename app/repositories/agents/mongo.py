from pymongo.collection import Collection

from app.entities.agents import AgentsEntity
from app.repositories.base.mongo import MongoRepository


class AgentsMongoRepository(MongoRepository[AgentsEntity]):
    def __init__(self, collection: Collection):
        super().__init__(collection, entity_cls=AgentsEntity)

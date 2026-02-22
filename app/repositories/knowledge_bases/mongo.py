from pymongo.collection import Collection

from app.entities.knowledge_bases import KnowledgeBasesEntity
from app.repositories.base.mongo import MongoRepository


class KnowledgeBasesMongoRepository(MongoRepository[KnowledgeBasesEntity]):
    def __init__(self, collection: Collection):
        super().__init__(collection, entity_cls=KnowledgeBasesEntity)

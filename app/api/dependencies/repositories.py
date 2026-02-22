from fastapi import Depends
from pymongo.collection import Collection

from app.api.dependencies.mongo import get_agents_collection, get_tools_collection, get_knowledge_bases_collection

from app.entities.agents import AgentsEntity
from app.entities.tools import ToolsEntity
from app.entities.knowledge_bases import KnowledgeBasesEntity
from app.repositories.base.mongo import MongoRepository


def get_agents_repository(
    collection: Collection = Depends(get_agents_collection),
) -> MongoRepository:
    return MongoRepository(collection=collection, entity_cls=AgentsEntity)


def get_tools_repository(
    collection: Collection = Depends(get_tools_collection),
) -> MongoRepository:
    return MongoRepository(collection=collection, entity_cls=ToolsEntity)


def get_knowledge_bases_repository(
    collection: Collection = Depends(get_knowledge_bases_collection),
) -> MongoRepository:
    return MongoRepository(collection=collection, entity_cls=KnowledgeBasesEntity)

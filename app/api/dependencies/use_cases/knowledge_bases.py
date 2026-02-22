from typing import Annotated

from fastapi import Depends

from app.api.dependencies.repositories import (
    get_knowledge_bases_repository,
)

from app.repositories.knowledge_bases.mongo import KnowledgeBasesMongoRepository
from app.use_cases.knowledge_bases.create_knowledge_base import CreateKnowledgeBaseUseCase
from app.use_cases.knowledge_bases.delete_knowledge_bases import DeleteKnowledgeBasesUseCase
from app.use_cases.knowledge_bases.list_knowledge_bases import ListKnowledgeBasesUseCase


def get_create_knowledge_base_use_case(
    knowledge_bases_repository: Annotated[KnowledgeBasesMongoRepository, Depends(get_knowledge_bases_repository)],
):
    return CreateKnowledgeBaseUseCase(
        knowledge_bases_repository=knowledge_bases_repository,
    )


def get_list_knowledge_bases_use_case(
    knowledge_bases_repository: Annotated[KnowledgeBasesMongoRepository, Depends(get_knowledge_bases_repository)],
):
    return ListKnowledgeBasesUseCase(knowledge_bases_repository=knowledge_bases_repository)


def delete_knowledge_bases_use_case(
    knowledge_bases_repository: Annotated[KnowledgeBasesMongoRepository, Depends(get_knowledge_bases_repository)],
):
    return DeleteKnowledgeBasesUseCase(knowledge_bases_repository=knowledge_bases_repository)

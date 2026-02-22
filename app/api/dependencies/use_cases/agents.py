from typing import Annotated

from fastapi import Depends

from app.api.dependencies.repositories import (
    get_agents_repository,
)

from app.repositories.agents.mongo import AgentsMongoRepository
from app.use_cases.agents.create_agent import CreateAgentUseCase
from app.use_cases.agents.delete_agents import DeleteAgentsUseCase
from app.use_cases.agents.list_agents import ListAgentsUseCase


def get_create_agent_use_case(
    agents_repository: Annotated[AgentsMongoRepository, Depends(get_agents_repository)],
):
    return CreateAgentUseCase(
        agents_repository=agents_repository,
    )


def get_list_agents_use_case(
    agents_repository: Annotated[AgentsMongoRepository, Depends(get_agents_repository)],
):
    return ListAgentsUseCase(agents_repository=agents_repository)


def delete_agents_use_case(
    agents_repository: Annotated[AgentsMongoRepository, Depends(get_agents_repository)],
):
    return DeleteAgentsUseCase(agents_repository=agents_repository)

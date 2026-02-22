from typing import Any
from fastapi import APIRouter

from app.schemas.agents.agent_create import AgentResponseSchema
from app.schemas.agents.agents_list import AgentsListSchema

from .endpoints import (
    create_agent,
    delete_agents,
    list_agents,
)

router = APIRouter(prefix="/agents", tags=["Agents"])

router.add_api_route(
    "/",
    create_agent,
    methods=["POST"],
    name="Create Agent",
    description="Creates a new agent.",
    response_model=AgentResponseSchema,
)

router.add_api_route(
    "/",
    list_agents,
    methods=["GET"],
    name="List Agents",
    description="Returns the agents if parameters is provided.",
    response_model=AgentsListSchema,
)

router.add_api_route(
    "/",
    delete_agents,
    methods=["DELETE"],
    name="Delete Agents",
    description="Delete agent(s) of a specific _id.",
    response_model=Any,
)

from app.core.logging import get_logger
from app.exceptions.agents import AgentNotExists
from app.repositories.agents.mongo import AgentsMongoRepository
from app.schemas.agents.agent_create import (
    AgentSchema,
    AgentResponseSchema,
)

logger = get_logger("create_agent")


class CreateAgentUseCase:
    def __init__(
        self,
        agents_repository: AgentsMongoRepository,
    ):
        self.agents_repository = agents_repository

    def execute(self, agent_data: AgentSchema) -> AgentResponseSchema:
        logger.info(f"Creating agent with: {agent_data}")

        try:

            created_agent = self.agents_repository.create(
                agent_data.model_dump(by_alias=True, exclude_none=True)
            )

            logger.info(f"Agent created successfully with id: {created_agent.id}")
            return AgentResponseSchema(**created_agent.model_dump())

        except (
            AgentNotExists,
            TypeError,
        ) as e:
            logger.error(f"Failed to create agent: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating agent: {str(e)}")
            raise

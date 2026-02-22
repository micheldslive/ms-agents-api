from typing import Optional
from app.exceptions.http import SystemHttpException
from app.exceptions.agents import AgentNotExists
from app.repositories.agents.mongo import AgentsMongoRepository
from app.core.logging import get_logger
from fastapi import status

logger = get_logger("delete_agents")


class DeleteAgentsUseCase:
    def __init__(self, agents_repository: AgentsMongoRepository):
        self.agents_repository = agents_repository

    def execute(self, filters: Optional[dict]):
        logger.info(f"Deleting agent(s) with filters: {filters}")

        agents = self.agents_repository.count(filters=filters)

        if agents == 0:
            logger.warning(f"Agent(s) not found with filters: {filters}")
            raise AgentNotExists()

        try:
            result = self.agents_repository.delete_many(filters=filters)
        except Exception as e:
            logger.exception("Error while counting agents")
            raise

        if not result:  # garante que não é None
            raise SystemHttpException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code="DELETE_FAILED",
            )

        return {
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged,
        }

from app.entities.base import EntityBase
from app.schemas.agents.agent_create import AgentsAvatarSchema


class AgentsEntity(EntityBase):
    specialty: str
    name: str
    avatar: AgentsAvatarSchema
    enable: bool

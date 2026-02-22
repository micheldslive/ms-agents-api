from datetime import datetime

from pydantic import BaseModel


class AgentsAvatarSchema(BaseModel):
    image_url: str


class AgentSchema(BaseModel):
    specialty: str
    name: str
    avatar: AgentsAvatarSchema
    enable: bool


class AgentResponseSchema(AgentSchema):
    id: str
    created_at: datetime

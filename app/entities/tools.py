from typing import Any, Dict, List, Optional

from app.entities.base import EntityBase
from app.schemas.tools.tool_create import (
    ToolAuthSchema,
    ToolConfigSchema,
    ToolParameterSchema,
    ToolTypeEnum,
)


class ToolsEntity(EntityBase):
    name: str
    description: str
    type: ToolTypeEnum
    enable: bool
    config: Optional[ToolConfigSchema] = None
    parameters: Optional[List[ToolParameterSchema]] = None
    output_schema: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None

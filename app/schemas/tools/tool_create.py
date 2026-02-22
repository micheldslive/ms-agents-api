from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ToolTypeEnum(str, Enum):
    http = "http"
    function = "function"
    webhook = "webhook"
    custom = "custom"


class ToolHttpMethodEnum(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class ToolAuthSchema(BaseModel):
    type: str = Field(..., description="Auth type: bearer, api_key, basic, oauth2")
    token: Optional[str] = Field(None, description="Bearer/API Key token value")
    header_name: Optional[str] = Field(
        None, description="Header name used to send the API key (e.g. X-API-Key)"
    )


class ToolConfigSchema(BaseModel):
    url: Optional[str] = Field(None, description="The endpoint URL for HTTP tools")
    method: Optional[ToolHttpMethodEnum] = Field(
        None, description="HTTP method for HTTP tools"
    )
    headers: Optional[Dict[str, str]] = Field(
        default_factory=dict, description="Static headers to include in requests"
    )
    timeout_seconds: Optional[int] = Field(
        30, ge=1, le=300, description="Timeout in seconds for HTTP requests"
    )
    auth: Optional[ToolAuthSchema] = Field(
        None, description="Authentication configuration"
    )


class ToolParameterSchema(BaseModel):
    name: str = Field(..., description="Parameter name")
    type: str = Field(..., description="JSON Schema type: string, number, boolean, object, array")
    description: str = Field(..., description="Parameter description for the agent")
    required: bool = Field(True, description="Whether the parameter is required")
    default: Optional[Any] = Field(None, description="Default value if parameter is optional")
    enum: Optional[List[Any]] = Field(None, description="Allowed values (for enum types)")


class ToolSchema(BaseModel):
    name: str = Field(..., description="Tool name displayed to agents")
    description: str = Field(..., description="What this tool does (used by the agent to decide when to call it)")
    type: ToolTypeEnum = Field(..., description="Tool type: http, function, webhook, custom")
    enable: bool = Field(True, description="Whether the tool is active")
    config: Optional[ToolConfigSchema] = Field(
        None, description="Tool-specific configuration (URL, method, auth, etc.)"
    )
    parameters: Optional[List[ToolParameterSchema]] = Field(
        default_factory=list,
        description="Input parameters the agent must supply when calling this tool",
    )
    output_schema: Optional[Dict[str, Any]] = Field(
        None, description="JSON Schema describing the tool output structure"
    )
    tags: Optional[List[str]] = Field(
        default_factory=list, description="Tags for grouping and filtering tools"
    )


class ToolResponseSchema(ToolSchema):
    id: str
    created_at: datetime
    updated_at: datetime

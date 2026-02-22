from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv(".env", override=True)


class AppSettings(BaseSettings):
    IS_DEVELOPMENT: bool = True
    MONGODB_URL: str = ""
    BACKEND_CORS_ORIGINS: list[str] = Field(default_factory=lambda: ["*"])
    OPENAPI_PREFIX: str = Field(default_factory=lambda: "/")


settings = AppSettings()

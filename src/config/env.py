from pydantic_settings import BaseSettings, SettingsConfigDict


@lambda s: s()
class Settings(BaseSettings):
    BASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

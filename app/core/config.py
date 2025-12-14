from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "베지나이 1.0"

    TOSS_API_KEY: str

    # [Solapi 키 추가]
    SOLAPI_API_KEY: str
    SOLAPI_API_SECRET: str
    SENDER_PHONE: str

    DATABASE_URL: str
    MANAGER_PHONE: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()
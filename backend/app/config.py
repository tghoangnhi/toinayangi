from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "toinayangi"
    debug: bool = True
    database_url: str = "sqlite:///./toinayangi.db"
    upload_dir: str = "./uploads"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"

    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    grocery_cron_hour: int = 8
    grocery_cron_minute: int = 0

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()

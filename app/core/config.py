from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação carregadas via variáveis de ambiente."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "E-Commerce DevSecOps GCP API"
    app_version: str = "1.1.0"
    environment: str = "development"
    log_level: str = "INFO"

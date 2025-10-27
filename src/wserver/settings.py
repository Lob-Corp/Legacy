from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8080

    ssl_enabled: bool = False
    ssl_cert_path: str = "certs/cert.pem"
    ssl_key_path: str = "certs/key.pem"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix=""
    )


settings = Settings()

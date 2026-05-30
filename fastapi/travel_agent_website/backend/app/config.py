from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "PeaceTimeTravellers"
    api_prefix: str = "/api"
    db_user: str = "root"
    db_password: str = "rootpassword"
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "peacetimetravellers"
    jwt_secret_key: str = "change-this-secret"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60
    openai_api_key: str = ""

    class Config:
        env_file = ".env"

settings = Settings()

from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config("backend/.env")

PROJECT_NAME: str = "Phresh"
VERSION: str = "0.1.0"
API_PREFIX: str = "/api"

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)


# DATABASE SETTINGS
POSTGRES_USER: str = config("POSTGRES_USER",cast=str)
POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD",cast=Secret)
POSTGRES_SERVER: str = config("POSTGRES_SERVER",cast=str,default="db")
POSTGRES_PORT: str = config("POSTGRES_PORT",cast=str,default="5432")
POSTGRES_DB: str = config("POSTGRES_DB",cast=str)

# Database connection settings
DB_MIN_CONNECTIONS: int = config("DB_MIN_CONNECTIONS", cast=int, default=2)
DB_MAX_CONNECTIONS: int = config("DB_MAX_CONNECTIONS", cast=int, default=10)


DATABASE_URL: DatabaseURL = config("DATABASE_URL", 
                                   cast=DatabaseURL, 
                                   default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}")


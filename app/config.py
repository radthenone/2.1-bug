import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


class Config:
    FLASK_RUN_RELOAD = os.environ.get("FLASK_RUN_RELOAD", 1)  # add 0 to debug
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
    DEBUG = os.environ.get("DEBUG", True)
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "db")
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")
    POSTGRES_HOST_AUTH_METHOD = os.environ.get("POSTGRES_HOST_AUTH_METHOD", "trust")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5433)
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", 1)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI",
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        "SQLALCHEMY_TRACK_MODIFICATIONS", False
    )
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret")

    @classmethod
    def to_dict(cls):
        return {
            key: value
            for key, value in vars(cls).items()
            if not key.startswith("__") and not callable(value)
        }


config_dict = Config.to_dict()

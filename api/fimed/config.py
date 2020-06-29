from pathlib import Path

from pydantic import BaseSettings, AnyUrl

from fimed.logger import logger


class MongoDns(AnyUrl):
    allowed_schemes = {"mongodb"}
    user_required = True


class _Settings(BaseSettings):
    # api settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8080

    # for applications sub-mounted below a given URL path
    ROOT_PATH: str = ""

    # database connection
    MONGO_DNS: MongoDns = "mongodb://root:root@localhost:27017"

    class Config:
        if not Path(".env").is_file():
            logger.warning("⚠️ `.env` not found in current directory")
            logger.info("⚙️ Loading settings from environment")
        else:
            logger.info("⚙️ Loading settings from dotenv file")
        env_file = ".env"


settings = _Settings()

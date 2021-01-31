from minio import Minio
from fimed.config import settings
from fimed.logger import logger


def minio_connection():
    logger.debug("Connecting to minio")
    client = Minio(
        settings.MINNIO_CONN,
        access_key=settings.ACCESS_KEY,
        secret_key=settings.SECRET_KEY,
        secure=False,
)
    return client


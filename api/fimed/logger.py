import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {"default": {"format": "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",}},
    "handlers": {"default": {"formatter": "default", "class": "logging.StreamHandler", "stream": "ext://sys.stderr",}},
    "loggers": {"": {"handlers": ["default"], "level": "INFO", "propagate": True,}, "fimed": {"level": "DEBUG"},},
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("fimed")

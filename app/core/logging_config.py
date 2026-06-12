import logging
import logging.config
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "json": {
            "format": (
                '{"time": "%(asctime)s", '
                '"level": "%(levelname)s", '
                '"logger": "%(name)s", '
                '"message": "%(message)s", '
                '"module": "%(module)s", '
                '"line": %(lineno)d}'
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "standard": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        },
        "requests_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "requests.log",
            "maxBytes": 5_000_000,
            "backupCount": 5,
            "formatter": "json",
            "level": "INFO",
        },
        "analyzers_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "analyzers.log",
            "maxBytes": 5_000_000,
            "backupCount": 5,
            "formatter": "json",
            "level": "INFO",
        },
        "errors_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "errors.log",
            "maxBytes": 5_000_000,
            "backupCount": 5,
            "formatter": "json",
            "level": "ERROR",
        },
    },

    "loggers": {
        "uvicorn.access": {
            "handlers": ["console", "requests_file"],
            "level": "INFO",
            "propagate": False,
        },
        "analyzers": {
            "handlers": ["console", "analyzers_file"],
            "level": "INFO",
            "propagate": False,
        },
        "errors": {
            "handlers": ["console", "errors_file"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

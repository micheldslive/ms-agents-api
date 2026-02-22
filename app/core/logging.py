import sys
from loguru import logger
from app.core.settings import settings


def setup_logging():
    logger.remove()

    if settings.IS_DEVELOPMENT:
        logger.add(
            sys.stdout,
            level="DEBUG",
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}:{function}</cyan> | {message}",
            colorize=True,
            backtrace=True,
            diagnose=True,
        )
    else:
        logger.add(
            sys.stdout,
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message} | {extra}",
            colorize=False,
            serialize=False,
            enqueue=True,
        )

        logger.add(
            sys.stderr,
            level="ERROR",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message} | {extra}",
            colorize=False,
            serialize=False,
            enqueue=True,
        )


def get_logger(name: str | None = None):
    return logger.bind(module=name) if name else logger

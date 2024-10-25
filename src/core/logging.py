import logging
from functools import lru_cache

from config.settings import get_settings


@lru_cache()
def get_logger():
    settings = get_settings()

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    return logging.getLogger(__name__)

import logging
from rich.logging import RichHandler


def setup_logging():
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(RichHandler())
    log_level = logging.INFO
    root_logger.setLevel(log_level)

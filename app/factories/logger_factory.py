import logging
import inspect
from typing import Optional


class LoggerFactory:
    _loggers = {}

    @staticmethod
    def _get_caller_name() -> str:
        frame = inspect.stack()[2]
        module = inspect.getmodule(frame[0])
        return module.__name__ if module else "APP"

    @staticmethod
    def get_logger(
        name: Optional[str] = None, level: int = logging.INFO
    ) -> logging.Logger:
        name = name or LoggerFactory._get_caller_name()

        if name not in LoggerFactory._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(level)

            if not logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%H:%M:%S"
                )
                handler.setFormatter(formatter)
                logger.addHandler(handler)

            LoggerFactory._loggers[name] = logger

        return LoggerFactory._loggers[name]

import logging
import json
from datetime import datetime
import sys

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "level": record.levelname.lower(),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": "pass-gen",
            "message": record.getMessage(),
        }
        if hasattr(record, "extra_fields") and record.extra_fields:
            log_data.update(record.extra_fields)
        return json.dumps(log_data, ensure_ascii=False)


logger = logging.getLogger("pass-gen")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    logger.propagate = False


class StructuredLogger:
    def __init__(self, logger_instance):
        self._logger = logger_instance

    def info(self, message: str, **kwargs):
        self._logger.info(message, extra={"extra_fields": kwargs})

    def error(self, message: str, **kwargs):
        self._logger.error(message, extra={"extra_fields": kwargs})

    def warning(self, message: str, **kwargs):
        self._logger.warning(message, extra={"extra_fields": kwargs})


log = StructuredLogger(logger)

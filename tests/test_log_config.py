import json
import logging

from app.core.log_config import JsonFormatter, setup_logging


def test_json_formatter_outputs_valid_json():
    record = logging.LogRecord("jobhub", logging.INFO, __file__, 1, "request", None, None)
    record.extra_fields = {"status": 200}
    data = json.loads(JsonFormatter().format(record))
    assert data["message"] == "request"
    assert data["level"] == "INFO"
    assert data["status"] == 200


def test_setup_logging_installs_json_handler():
    setup_logging()
    handlers = logging.getLogger().handlers
    assert any(isinstance(h.formatter, JsonFormatter) for h in handlers)
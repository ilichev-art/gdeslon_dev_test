import logging
import io
import re
from typing import Optional

import colorlog

_logger_initialized = False


class InMemoryLogHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__()
        self.log_capture_string = io.StringIO()
        self.setStream(self.log_capture_string)

    def emit(self, record):
        super().emit(record)
        self.flush()

    def get_logs(self):
        return InMemoryLogHandler.__ansi_to_html(self.log_capture_string.getvalue())

    def clear_logs(self):
        self.log_capture_string.seek(0)
        self.log_capture_string.truncate()

    @staticmethod
    def __ansi_to_html(logs):
        ansi_to_html_map = {
            r'\x1b\[37m': '<span style="color: white;">',
            r'\x1b\[1;36m': '<span style="color: cyan; font-weight: bold;">',
            r'\x1b\[1;32m': '<span style="color: green; font-weight: bold;">',
            r'\x1b\[1;33m': '<span style="color: yellow; font-weight: bold;">',
            r'\x1b\[1;31m': '<span style="color: red; font-weight: bold;">',
            r'\x1b\[1;37;41m': '<span style="color: white; background-color: red; font-weight: bold;">',
            r'\x1b\[36m': '<span style="color: cyan;">',
            r'\x1b\[32m': '<span style="color: green;">',
            r'\x1b\[33m': '<span style="color: yellow;">',
            r'\x1b\[31m': '<span style="color: red;">',
            r'\x1b\[37;41m': '<span style="color: white; background-color: red;">',
            r'\x1b\[0m': '</span>'
        }

        for ansi, html in ansi_to_html_map.items():
            logs = re.sub(ansi, html, logs)

        timestamp_pattern = r'(\d{4}-\d{2}-\d{2} )(\d{2}:\d{2}:\d{2})'
        logs = re.sub(timestamp_pattern, r'<br>\2', logs)
        logs = logs.replace('<br>', '', 1)

        return f"<html><body style='background-color: #333; color: white;'>{logs}</body></html>"


_memory_handler: Optional[InMemoryLogHandler] = None


def setup_colored_logging():
    global _memory_handler
    logger = logging.getLogger(__name__)

    formatter = colorlog.ColoredFormatter(
        '\n%(white)s%(asctime)-8s %(log_color)s%(levelname)-8s%(reset)s%(message_log_color)s%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'bold_cyan',
            'INFO': 'bold_green',
            'WARNING': 'bold_yellow',
            'ERROR': 'bold_red',
            'CRITICAL': 'bold_red,bg_white',
        },
        secondary_log_colors={
            'message': {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red',
            }
        }
    )

    # Console handler for colored output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # In-memory log handler for capturing logs
    _memory_handler = InMemoryLogHandler()
    _memory_handler.setFormatter(formatter)
    logger.addHandler(_memory_handler)

    logger.setLevel(logging.DEBUG)

    return logger


def _get_logger(name):
    global _logger_initialized
    if not _logger_initialized:
        setup_colored_logging()
        _logger_initialized = True
    return logging.getLogger(name)


def get_log_memo():
    global _memory_handler
    return _memory_handler


log = _get_logger(__name__)

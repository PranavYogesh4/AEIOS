
import logging
import sys


class AEIOSLogger:

    def __init__(self):
        self.logger = logging.getLogger("AEIOS")

        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s",
                "%H:%M:%S"
            )

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)

            self.logger.addHandler(console_handler)

    def info(self, message, *args, **kwargs):
        self.logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self.logger.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self.logger.error(message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        self.logger.debug(message, *args, **kwargs)

    def exception(self, message, *args, **kwargs):
        self.logger.exception(message, *args, **kwargs)


logger = AEIOSLogger()

import logging


# pylint: disable=too-few-public-methods
class CustomLogger:
    """Custom logger with formatter and console handler."""

    def __init__(self) -> None:
        """
        Initializes the custom logger.
        """
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        consoleHandler = logging.StreamHandler()

        consoleHandler.setFormatter(formatter)

        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(consoleHandler)

    def get_logger(self) -> logging.Logger:
        """
        Get the custom logger instance.
        :return: logging.Logger instance.
        """
        return self.logger

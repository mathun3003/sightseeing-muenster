import logging


# pylint: disable=too-few-public-methods
class CustomLogger:
    """Custom logger with formatter and console handler."""

    def __init__(self) -> None:
        """
        Initializes the custom logger.
        """
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        self.log = logging.getLogger(__name__)
        self.log.addHandler(console_handler)

    @property
    def logger(self) -> logging.Logger:
        """
        Get the custom logger instance.
        :return: logging.Logger instance.
        """
        return self.log

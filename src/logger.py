"""
Logging utilities for Facebook Automation
"""

import logging
import os
from datetime import datetime


class Logger:
    """Centralized logging configuration"""

    _logger = None

    @classmethod
    def get_logger(cls, name: str = "fb_automation") -> logging.Logger:
        """Get or create logger instance"""
        if cls._logger is not None:
            return cls._logger

        # Create logs directory if it doesn't exist
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Remove existing handlers
        logger.handlers = []

        # File handler
        log_file = f"{log_dir}/facebook_automation_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        cls._logger = logger
        return logger

    @classmethod
    def info(cls, message: str) -> None:
        """Log info message"""
        cls.get_logger().info(message)

    @classmethod
    def debug(cls, message: str) -> None:
        """Log debug message"""
        cls.get_logger().debug(message)

    @classmethod
    def warning(cls, message: str) -> None:
        """Log warning message"""
        cls.get_logger().warning(message)

    @classmethod
    def error(cls, message: str) -> None:
        """Log error message"""
        cls.get_logger().error(message)

    @classmethod
    def critical(cls, message: str) -> None:
        """Log critical message"""
        cls.get_logger().critical(message)

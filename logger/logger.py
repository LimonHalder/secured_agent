"""
Security Logging Utility

Provides centralized logging functions for input/output, threats, errors, and warnings.
Writes structured logs to a UTF-8 encoded log file named 'security.log'.

Author: Limon Halder
"""

import logging
from typing import Any

# Configure logger
logger = logging.getLogger("SecurityLogger")
logger.setLevel(logging.DEBUG)

# Define log message format
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

# Log to a file with UTF-8 encoding
file_handler = logging.FileHandler("security.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def log_input(text: Any) -> None:
    """
    Logs user input sent to the system.

    Args:
        text (Any): Input message or object.
    """
    safe_text = str(text)
    logger.info(f"Input: {safe_text}")


def log_output(text: Any) -> None:
    """
    Logs system output returned to the user.

    Args:
        text (Any): Output message or object.
    """
    safe_text = str(text)
    logger.info(f"Output: {safe_text}")


def log_error(error_message: Any) -> None:
    """
    Logs an error message.

    Args:
        error_message (Any): Exception message or string description.
    """
    safe_message = str(error_message)
    logger.error(f"Error: {safe_message}")


def log_warning(warning_message: Any) -> None:
    """
    Logs a warning message.

    Args:
        warning_message (Any): Warning description.
    """
    safe_message = str(warning_message)
    logger.warning(f"Warning: {safe_message}")


def log_threat(threat_type: str, text: Any, stage: str) -> None:
    """
    Logs a detected threat incident with metadata.

    Args:
        threat_type (str): The type of threat (e.g., 'Prompt Injection').
        text (Any): The raw text that triggered the detection.
        stage (str): 'input' or 'output' — stage where threat was found.
    """
    safe_text = str(text)
    logger.warning(f"{threat_type} Threat Detected during {stage}: {safe_text}")

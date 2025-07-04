import os
from dotenv import load_dotenv
from logger.logger import logger


def load_environment() -> None:
    """
    Load environment variables from a .env file.

    Logs success or failure of the operation.
    """
    try:
        load_dotenv()
        logger.info("Environment variables loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load environment variables: {e}")

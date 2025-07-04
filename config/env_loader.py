import os
from dotenv import load_dotenv
from logger.logger import logger

def load_environment() -> None:
    try:
        load_dotenv()
        logger.info("Environment variables loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load environment variables: {e}")

import os
from typing import Optional
from langchain_tavily import TavilySearch
from logger.logger import logger


def init_search_tool() -> Optional[TavilySearch]:
    """
    Initializes the TavilySearch tool with predefined parameters.

    Returns:
        Optional[TavilySearch]: An instance of TavilySearch if initialization succeeds; otherwise, None.
    """
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            logger.error("TAVILY_API_KEY not found in environment variables.")
            return None

        search_tool = TavilySearch(
            max_results=5,
            topic="general",
            tavily_api_key=api_key
        )

        logger.info("TavilySearch tool initialized successfully.")
        return search_tool

    except Exception as e:
        logger.exception(f"TavilySearch initialization failed.")
        return None

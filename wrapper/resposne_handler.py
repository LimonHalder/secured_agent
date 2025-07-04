"""
Response Handler Module

Provides a utility to handle and log agent responses during a streaming session.
This is helpful for debugging, logging, and monitoring the LLM's output in production environments.

Author: Limon Halder
"""

from typing import Any

from logger.logger import log_output


def response_handler(message: Any) -> str:
    """
    Handles the output of an agent's response message during streaming.

    Logs the response and prints it to the console.

    Args:
        message (Any): A message object or string-like object. 
                       Typically has a `content` attribute if coming from LangChain or similar frameworks.

    Returns:
        str: The string content extracted from the message.
    """
    content: str = getattr(message, "content", str(message))
    log_output(f"Response Handler received: {content}")
    print(f"Agent Response: {content}")
    return content

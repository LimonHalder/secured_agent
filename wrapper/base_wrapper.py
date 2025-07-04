"""
SecureAgentWrapper: A security wrapper for streaming LLM agents.

This module provides a wrapper class for any agent supporting a `stream` method.
It adds input/output logging, threat detection, and runtime tracking to enhance
security and observability in production environments.

Author: Limon Halder
"""

import os
import sys
import time
from typing import Any, Dict, Generator, List, Optional, Union

# Allow imports from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wrapper.threat_detector import check_for_threats
from logger.logger import logger, log_input, log_output, log_threat


def extract_text_from_messages(
    messages: Union[List[Any], Dict[str, Any], Any]
) -> str:
    """
    Extracts and concatenates content text from LLM-style message objects.

    Args:
        messages (Union[List[Any], Dict[str, Any], Any]): A list or single message object.

    Returns:
        str: The combined textual content of the messages.
    """
    if not messages:
        return ""

    if isinstance(messages, list):
        texts = []
        for msg in messages:
            if isinstance(msg, dict) and "content" in msg:
                texts.append(msg["content"])
            elif hasattr(msg, "content"):
                texts.append(msg.content)
            else:
                texts.append(str(msg))
        return " ".join(texts)

    if hasattr(messages, "content"):
        return messages.content

    return str(messages)


class SecureAgentWrapper:
    """
    A wrapper for secure, auditable streaming from an LLM-based agent.

    Responsibilities:
    - Logs incoming messages
    - Detects threats in input and output
    - Tracks performance metrics
    - Yields safe output back to caller

    Attributes:
        agent (Any): The underlying LLM agent that supports a `.stream()` method.
    """

    def __init__(self, agent: Any):
        """
        Initialize the SecureAgentWrapper.

        Args:
            agent (Any): An object that implements a `stream()` generator.
        """
        self.agent = agent

    def stream(
        self, *args: Any, **kwargs: Any
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Securely stream responses from the agent with input/output threat checks.

        Args:
            *args (Any): Positional arguments to pass to the agent's stream method.
            **kwargs (Any): Keyword arguments, must include `messages` key or
                pass messages as first arg.

        Yields:
            Dict[str, Any]: A dictionary containing streaming message data from the agent.
        """
        input_data = kwargs.get("messages") or args[0].get("messages")
        log_input(input_data)

        if not check_for_threats(input_data, stage="input"):
            log_threat("Blocked input due to threat detection", input_data, "input")
            yield {
                "messages": [
                    {
                        "role": "system",
                        "content": "⚠️ Input blocked due to security concerns.",
                    }
                ]
            }
            return

        message_count = 0
        start_time = time.time()

        try:
            for step in self.agent.stream(*args, **kwargs):
                message_count += 1

                try:
                    output_data = step.get("messages")
                    output_text = extract_text_from_messages(output_data)

                    log_output(output_data)

                    if not check_for_threats(output_text, stage="output"):
                        log_threat(
                            "Blocked output due to threat detection",
                            output_text,
                            "output",
                        )
                        yield {
                            "messages": [
                                {
                                    "role": "system",
                                    "content": "⚠️ Output blocked due to security concerns.",
                                }
                            ]
                        }
                        return

                    yield step

                except Exception as yield_error:
                    logger.exception(f"Error during streaming yield: {yield_error}")
        finally:
            elapsed_time = time.time() - start_time
            logger.info(
                f"Stream completed in {elapsed_time:.2f} seconds | "
                f"Messages processed: {message_count}"
            )

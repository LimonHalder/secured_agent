from typing import Any, Dict, List, TypedDict
from langchain_core.messages import AIMessage, BaseMessage
from logger.logger import log_input, log_output, logger


class StateType(TypedDict):
    messages: List[BaseMessage]


class LLMNode:
    """
    A callable wrapper class for invoking an LLM in a structured LangChain workflow.

    Attributes:
        llm: An LLM instance with an `invoke()` method that accepts a list of messages.
    """

    def __init__(self, llm_instance: Any):
        """
        Initializes the LLMNode.

        Args:
            llm_instance: The language model instance (e.g., ChatOpenAI) to invoke.
        """
        self.llm = llm_instance

    def __call__(self, state: StateType) -> StateType:
        """
        Invokes the LLM with the current conversation state.

        Args:
            state (StateType): A dictionary containing a list of messages under the
                "messages" key.

        Returns:
            StateType: A new state dictionary with the response appended as the latest message.
        """
        try:
            last_msg = state["messages"][-1]
            input_text = getattr(last_msg, "content", str(last_msg))
            log_input(input_text)

            response: AIMessage = self.llm.invoke(state["messages"])
            log_output(response.content)

            return {"messages": [response]}

        except Exception as e:
            logger.exception("LLM invocation failed.")
            return {
                "messages": [
                    AIMessage(
                        content="⚠️ An internal error occurred during LLM processing."
                    )
                ]
            }

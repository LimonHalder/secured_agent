"""
LangGraph Agent Builder Module

This module constructs a LangGraph agent using a provided LLM node and an optional search tool.
It defines the message state structure, builds nodes and edges for LangGraph, and compiles the graph.

Author: Limon Halder
"""

from typing import Annotated, TypedDict, Optional, Union
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.runnables import Runnable
from langchain_core.tools import Tool
from logger.logger import logger


class State(TypedDict):
    """
    Message state structure for LangGraph.

    Attributes:
        messages (list): A list of messages passed between nodes in the graph.
    """
    messages: Annotated[list, add_messages]


def build_agent(
    llm_node: Runnable,
    search_tool: Optional[Tool] = None
) -> Optional[Runnable]:
    """
    Constructs a LangGraph agent by wiring up LLM and tool nodes.

    Args:
        llm_node (Runnable): The node responsible for LLM interactions.
        search_tool (Optional[Tool]): An optional tool (e.g., search) to bind with the graph.

    Returns:
        Optional[Runnable]: A compiled LangGraph agent ready for execution, or None if an error occurs.
    """
    try:
        # Initialize graph with state schema
        graph = StateGraph(State)

        # Initialize tool node (empty if no tool provided)
        tool_node = ToolNode([search_tool]) if search_tool else ToolNode([])

        # Add nodes and edges to the graph
        graph.add_node("llm", llm_node)
        graph.add_node("tools", tool_node)
        graph.add_edge(START, "llm")
        graph.add_conditional_edges("llm", tools_condition)
        graph.add_edge("tools", "llm")

        # Compile and return the agent
        agent = graph.compile()
        logger.info("LangGraph agent compiled successfully.")
        return agent

    except Exception as e:
        logger.error(f"Failed to build agent: {e}")
        return None

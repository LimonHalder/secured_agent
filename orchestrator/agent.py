# """
# Main LLM Agent Orchestrator

# Initializes:
# - Environment variables
# - LLM (ChatGroq)
# - Tool (TavilySearch)
# - LangGraph with tool routing
# - Secure streaming agent wrapper

# Handles:
# - Logging for input/output
# - Threat detection
# - Response handling

# Author: Limon Halder
# """

# import os
# import sys
# from typing import Annotated

# # Set up import path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from dotenv import load_dotenv
# from typing_extensions import TypedDict

# from langgraph.graph import StateGraph, START, END
# from langgraph.graph.message import add_messages
# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.prebuilt import ToolNode, tools_condition

# from langchain_openai import ChatOpenAI
# from langchain_groq import ChatGroq
# from langchain_tavily import TavilySearch
# from langchain_core.messages import HumanMessage, AIMessage

# from wrapper.base_wrapper import SecureAgentWrapper
# from wrapper.response_handler import response_handler
# from logger.logger import logger, log_input, log_output, log_threat

# # -------------------------------------------------------------------
# # Load environment variables
# # -------------------------------------------------------------------
# try:
#     load_dotenv()
#     logger.info("Loaded .env variables successfully.")
# except Exception as e:
#     logger.error(f"Failed to load .env file: {e}")

# # -------------------------------------------------------------------
# # Initialize tools (Tavily)
# # -------------------------------------------------------------------
# try:
#     search_tool = TavilySearch(
#         max_results=5,
#         topic="general",
#         tavily_api_key=os.getenv("TAVILY_API_KEY")
#     )
#     logger.info("TavilySearch tool initialized.")
# except Exception as e:
#     logger.error(f"Failed to initialize TavilySearch: {e}")
#     search_tool = None

# # -------------------------------------------------------------------
# # Initialize LLM (ChatGroq)
# # -------------------------------------------------------------------
# try:
#     llm = ChatGroq(
#         temperature=0,
#         model_name="llama3-70b-8192",
#         groq_api_key=os.getenv("GROQ_API_KEY")
#     )
#     logger.info("ChatGroq LLM initialized.")
# except Exception as e:
#     logger.error(f"Failed to initialize ChatGroq: {e}")
#     llm = None

# # -------------------------------------------------------------------
# # Define message state structure
# # -------------------------------------------------------------------
# class State(TypedDict):
#     messages: Annotated[list, add_messages]

# # -------------------------------------------------------------------
# # Define LLM Node
# # -------------------------------------------------------------------
# class LLMNode:
#     """
#     Node responsible for handling LLM invocation and response routing.
#     """

#     def __init__(self, llm_instance):
#         self.llm = llm_instance

#     def __call__(self, state: State) -> dict:
#         try:
#             last_msg = state["messages"][-1]
#             input_text = last_msg.content if hasattr(last_msg, "content") else str(last_msg)
#             log_input(input_text)

#             response = self.llm.invoke(state["messages"])

#             if hasattr(response, "tool_calls") and response.tool_calls:
#                 logger.info(f"LLM tool call triggered: {response.tool_calls}")

#             log_output(response.content)
#             return {"messages": [response]}

#         except Exception as e:
#             logger.error(f"LLM invocation failed: {e}")
#             return {"messages": [AIMessage(content="An error occurred while processing your request.")]}

# # -------------------------------------------------------------------
# # Bind tools to LLM
# # -------------------------------------------------------------------
# try:
#     bound_llm = llm.bind_tools([search_tool]) if search_tool else llm
#     llm_node = LLMNode(bound_llm)
#     logger.info("Tools bound to LLM successfully.")
# except Exception as e:
#     logger.error(f"Failed to bind tools to LLM: {e}")
#     llm_node = LLMNode(llm)

# # -------------------------------------------------------------------
# # Setup ToolNode
# # -------------------------------------------------------------------
# tool_node = ToolNode([search_tool]) if search_tool else ToolNode([])

# # -------------------------------------------------------------------
# # Build LangGraph
# # -------------------------------------------------------------------
# graph_builder = StateGraph(State)
# graph_builder.add_node("llm", llm_node)
# graph_builder.add_node("tools", tool_node)
# graph_builder.add_edge(START, "llm")
# graph_builder.add_conditional_edges("llm", tools_condition)
# graph_builder.add_edge("tools", "llm")

# # -------------------------------------------------------------------
# # Compile Graph Agent
# # -------------------------------------------------------------------
# try:
#     agent = graph_builder.compile()
#     logger.info("LangGraph compiled successfully.")
# except Exception as e:
#     logger.error(f"Failed to compile LangGraph: {e}")
#     agent = None

# # -------------------------------------------------------------------
# # Stream Messages with Secure Wrapper
# # -------------------------------------------------------------------
# if agent:
#     try:
#         secure_agent = SecureAgentWrapper(agent)
#         logger.info("SecureAgentWrapper initialized.")

#         # Example request
#         for step in secure_agent.stream(
#             {"messages": "Weather in khulna?"},
#             stream_mode="values",
#         ):
#             msg = step["messages"][-1]
#             logger.info(f"Agent Step: {type(msg).__name__} | Content: {getattr(msg, 'content', str(msg))}")

#             # Response handler (console + logging)
#             response_handler(msg)

#         logger.info("Streaming completed.")

#     except Exception as e:
#         logger.error(f"Secure agent streaming failed: {e}")

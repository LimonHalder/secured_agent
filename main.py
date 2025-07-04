import os
from orchestrator.llm_node import LLMNode
from orchestrator.tool_initializer import init_search_tool
from orchestrator.agent_builder import build_agent
from wrapper.base_wrapper import SecureAgentWrapper
from wrapper.resposne_handler import response_handler
from config.env_loader import load_environment
from langchain_groq import ChatGroq
from logger.logger import logger

def main():
    load_environment()

    # Initialize tools and LLM
    search_tool = init_search_tool()

    try:
        llm = ChatGroq(
            temperature=0,
            model_name="llama3-70b-8192",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        logger.info("LLM initialized.")
    except Exception as e:
        logger.error(f"LLM init failed: {e}")
        return

    # Bind tools and build agent
    bound_llm = llm.bind_tools([search_tool]) if search_tool else llm
    llm_node = LLMNode(bound_llm)
    agent = build_agent(llm_node, search_tool)

    if not agent:
        logger.error("Agent creation failed.")
        return

    secure_agent = SecureAgentWrapper(agent)

    # Example interaction
    for step in secure_agent.stream({"messages": "Weather in Khulna?"}, stream_mode="values"):
        msg = step["messages"][-1]
        logger.info(f"Response: {getattr(msg, 'content', str(msg))}")
        response_handler(msg)

if __name__ == "__main__":
    main()

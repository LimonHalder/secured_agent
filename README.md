# Secure LangGraph Agent

This project is a secure, modular AI agent built using [LangChain](https://github.com/langchain-ai/langchain) and [LangGraph](https://github.com/langchain-ai/langgraph). It supports tool integration, input/output monitoring, and threat detection, making it suitable for production environments.

## Project Overview

The agent is designed to be flexible and extensible. It combines LangChain’s tool chaining with LangGraph’s state-based control flow. Key features include:

- Secure question answering using an LLM  
- Integration with external tools like Tavily Search  
- Input/output threat detection  
- Structured logging for all actions and events

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/LimonHalder/secured_agent.git
cd secured_agent
```

Set Up a Virtual Environment
```bash
python -m venv venv
# For Windows:
venv\Scripts\activate
# For macOS/Linux:
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Configure Environment Variables
Create a .env file in the root directory and add your API keys:
```bash
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Running the Agent
Running the Main Agent
This will start the agent and allow it to process user inputs and make use of tools like Tavily Search.

```bash

python main.py
```

Running Threat Detection Tests
This script tests whether malicious or suspicious inputs are correctly identified and blocked.

```bash
python tests\test_threat.py
Test results will be printed and also logged.
```

Logging and Monitoring
All activity—such as user inputs, LLM responses, detected threats, errors, and warnings—is saved to a file called security.log in the root directory. Each log entry includes a timestamp and severity level.

To view the logs in real-time using PowerShell:

```bash

Get-Content .\security.log -Wait
```
This helps with debugging and keeping track of system behavior.

Tech Stack
LangChain – For managing chains and tool calls

LangGraph – For defining stateful agent workflows

Tavily Search – For augmenting LLMs with real-time web search

SecureAgentWrapper – Custom wrapper for logging and threat filtering

Python Logging – Centralized logging configuration

Project Structure

SECURITY_WRAPPER/
├── config/
│   └── env_loader.py               # Loads environment variables from .env
├── logger/
│   ├── __init__.py
│   └── logger.py                   # Logging setup and helpers
├── orchestrator/
│   ├── __init__.py
│   ├── agent_builder.py           # LangGraph agent flow builder
│   ├── llm_node.py                # LangGraph LLM node logic
│   └── tool_initializer.py        # Tool initialization (e.g., Tavily)
├── tests/
│   └── test_threat.py             # Threat detection test cases
├── wrapper/
│   ├── __init__.py
│   ├── base_wrapper.py            # Agent wrapper with threat detection
│   ├── response_handler.py        # Post-process agent outputs
│   ├── threat_detector.py         # Core threat detection logic
│   └── config.yml                 # Configuration for threat patterns
├── .env                           # Environment variables (ignored in git)
├── .gitignore
├── main.py                        # Entry point to run the agent
├── requirements.txt               # Python dependencies
├── security.log                   # Runtime logs (auto-generated)
└── README.md

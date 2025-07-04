
````markdown
# 🧠 Secure LangGraph Agent

A secure, modular AI agent powered by [LangChain](https://github.com/langchain-ai/langchain) and [LangGraph](https://github.com/langchain-ai/langgraph), with built-in support for tool use, threat detection, and structured logging.

## 📂 Project Overview

This project combines the flexibility of LangChain with the stateful flow control of LangGraph. It supports:

- ✅ Secure question answering via LLM  
- 🔍 Tool-based queries (e.g., Tavily Search)  
- ⚠️ Threat detection and validation  
- 📊 Structured logging and error tracking  

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/LimonHalder/secured_agent.git
cd secured_agent
````

### 2. Setup Python Environment

```bash
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory with the following:

```env
GROQ_API_KEY=your_GROQ_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## 🧪 Running the Agent

### ▶️ Run Main Agent (Q\&A + Tools)

To start the agent for general question-answering and tool-based tasks:

```bash
python main.py
```

This script initializes the LangGraph-powered agent and handles input/output with integrated tools.

### 🛡️ Run Threat Checker

To test the agent's response to potentially malicious or suspicious inputs:

```bash
python run_threat_tests.py
```

This will trigger the security wrappers and log results accordingly.

## 🧰 Tech Stack

* **LangChain** – LLM chains and tool integrations
* **LangGraph** – State-based LLM orchestration
* **TavilySearch** – External search API integration
* **Custom Wrappers** – SecureAgentWrapper, threat detector
* **Python Logging** – Centralized, formatted logs

## 📁 File Structure

```
SECURITY_WRAPPER/
├── config/
│ └── env_loader.py # Loads .env variables
├── logger/
│ ├── init.py
│ └── logger.py # Logging configuration
├── orchestrator/
│ ├── init.py
│ ├── agent_builder.py # Constructs LangGraph agent flow
│ ├── llm_node.py # LLM-related LangGraph node logic
│ └── tool_initializer.py # Tool (e.g., Tavily) initialization
├── tests/
│ └── test_threat.py # Unit tests for threat checking
├── wrapper/
│ ├── init.py
│ ├── base_wrapper.py # Secure wrapper for agent protection
│ ├── config.yml # Threat detection config
│ ├── response_handler.py # Output post-processing logic
│ └── threat_detector.py # Detects malicious or unsafe queries
├── .env # Environment variables (not committed)
├── .gitignore
├── main.py # Run the main LangGraph agent
├── requirements.txt # Python dependencies
├── security.log # Logs from threat and usage
└── README.md
```

## 📄 .gitignore

```gitignore
.env
__pycache__/
*.pyc
venv/
logs/
.vscode/
```

## 📃 License

MIT License

```

```

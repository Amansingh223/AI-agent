# Deep Research AI Agent

A dual-agent AI system for deep online research and intelligent answer generation, built using **LangGraph**, **LangChain**, **Tavily API**, and **Together AI**.

# Features

-  **Web Research Agent**: Uses the Tavily API to search the internet and gather relevant information.
-  **Answer Drafting Agent**: Uses a powerful open-source LLM from Together AI to generate accurate and well-cited responses.
-  **LangGraph Workflow**: Implements a dual-node graph where each agent is a separate node, connected in a clean pipeline.
-  Fully customizable and free-tier friendly.

# How It Works

1. **User asks a question**.
2. The **Research Agent** queries Tavily for relevant articles and extracts source content.
3. The **Answer Agent** uses a prompt template to craft a 3-paragraph answer using the extracted content.
4. The system prints the answer along with the sources.

##  Technologies

- **LangGraph** – Orchestrates the agent flow using a state graph.
- **LangChain** – Manages LLMs and prompt templating.
- **Tavily API** – Provides real-time web search and content scraping.
- **Together AI** – Supplies the open-source LLM (`Mixtral-8x7B-Instruct-v0.1`).

##  Installation

python -m venv env

env\Scripts\activate# On Windows

pip install -r requirements.txt

You'll need API keys for:

Together AI

Tavily

set TOGETHER_API_KEY=your_together_key

python main.py



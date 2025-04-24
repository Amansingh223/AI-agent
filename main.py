import os
import requests
from typing import TypedDict, List
from langchain_together import Together
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph


# Get environment variables
together_api_key = os.getenv("TOGETHER_API_KEY")
tavily_api_key = "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"
search_query = "example query"

url = f"https://api.tavily.com/search?q={search_query}"
headers = {
    "Authorization": f"Bearer {tavily_api_key}",
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    results = response.json()
    print(results)
else:
    print("Error:", response.status_code)


# Check for missing environment variables
if not together_api_key:
    raise ValueError("Missing TOGETHER_API_KEY environment variable.")
if not tavily_api_key:
    raise ValueError("Missing TAVILY_API_KEY environment variable.")

# ✅ Initialize Together AI LLM (free model)
llm = Together(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    together_api_key=together_api_key  # Using the correct variable
)

# ✅ Tavily tool for search
def tavily_search(query, max_results=3):
    url = "https://api.tavily.com/search"
    headers = {"Authorization": f"Bearer {tavily_api_key}", "Content-Type": "application/json"}
    data = {"query": query, "max_results": max_results}
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print("Tavily API Error:", response.status_code)
        return []

# ✅ Define system state
class State(TypedDict):
    question: str
    search_results: List[dict]
    answer: str

# 🔍 Research Step
def research_step(state):
    print("🔍 Researching...")
    results = tavily_search(state["question"], max_results=3)
    return {"search_results": results}

# ✍️ Answer Step
def answer_step(state):
    print("✍️ Drafting answer...")
    sources = "\n".join(
        [f"[{i+1}] {r['content']}" for i, r in enumerate(state["search_results"])]
    )
    prompt = ChatPromptTemplate.from_template(""" 
    Write a concise 3-paragraph answer to: {question}
    using these sources: {sources}
    Include [source numbers] for references.
    """)
    chain = prompt | llm
    response = chain.invoke({
        "question": state["question"],
        "sources": sources
    })
    return {"answer": response.content if hasattr(response, "content") else str(response)}


# 🔄 Build the graph
workflow = StateGraph(State)
workflow.add_node("research", research_step)
workflow.add_node("generate_answer", answer_step)
workflow.add_edge("research", "generate_answer")
workflow.set_entry_point("research")
workflow.set_finish_point("generate_answer")

# ✅ Compile system
research_system = workflow.compile()

# 🧠 Ask a question
def ask_question(question):
    result = research_system.invoke({"question": question})
    print("\n🌟 Answer:")
    print(result["answer"])
    print("\n📚 Sources:")
    for i, source in enumerate(result["search_results"], 1):
        print(f"{i}. {source['url']}")

# 🎯 Example
ask_question("tell me about pahalgam attack in india on 22 april 2025 ?")

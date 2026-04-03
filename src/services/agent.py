import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

# from src.services.tools import retrieve_docs
from src.tools.fts_search_tool import fts_search
from src.tools.hybrid_search_tool import _hybrid_search
from src.tools.vector_search_tool import query_documents
from langchain_core.tools import tool

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite-preview",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

system_prompt = """
You are an intelligent credit risk assessment and loan underwriting agent assistant.

You have access to the tools:
- fts_search_tool, hybrid_search_tool, vector_search_tool

STRICT RULES:

1. ALWAYS call the tools before answering
2. Use ONLY tool output
3. If tool returns "No relevant data found", return that

Extract:
- document_name from Source
- page_no from Page
- section from Section
- And the retrieved question and answers from chunks as list of chunks

FINAL OUTPUT MUST BE JSON:

{
  "query": "<user_query>",
  "answer": "<final answer>",
  "document_name": "<source>",
  "page_no": "<page>",
  "section": "<section>",
  "chunks": "<[chunks]>"
}

Include ALL citations.
Do NOT hallucinate.
Output ONLY JSON.
"""

@tool
def fts_search_tool(query: str):
    """
    It is best suited for identifying specific credit risk policy names, frameworks, models, acronyms, fixed terminology, document titles, and section headers.
    Use this tool when the user query contains precise or well‑defined credit risk terms (e.g., PD, LGD, exposure limits, policy names).
    Do not use this tool for conversational, explanatory, or scenario‑based credit risk questions.
   """
    return fts_search(query)

@tool
def hybrid_search_tool(query: str):
    """
    Use this tool when the query requires both exact credit risk terminology matching and contextual understanding.
    It is best suited for long, complex, or ambiguous credit risk questions, including scenario‑based or decision‑oriented queries.
    This tool combines keyword‑based search with semantic similarity to retrieve the most relevant credit risk policies and rules.
    Use this tool when it is unclear whether a purely keyword or purely semantic search would be sufficient.
   """
    return _hybrid_search(query)

@tool
def query_documents_tool(query: str):
    """
    Use this tool for semantic similarity search over Credit Risk documents.
    It is best suited for natural‑language and concept‑based credit risk questions.
    Use this tool when the user is seeking explanations, interpretations of policy intent, or descriptions of credit risk processes and frameworks.
    Do not rely on exact keyword or acronym matching when using this tool; focus on conceptual relevance instead.
   """
    return query_documents(query)

agent = create_agent(
    model=llm,
    tools=[hybrid_search_tool, fts_search_tool, query_documents_tool],
    system_prompt=system_prompt
)

def query_rag(user_query: str):
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": user_query}
        ]
    })

    return response

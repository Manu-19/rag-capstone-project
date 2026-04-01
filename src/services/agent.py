import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

# from src.services.tools import retrieve_docs
from src.tools.fts_search_tool import fts_search
from src.tools.hybrid_search_tool import _hybrid_search
from src.tools.vector_search_tool import query_documents

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

agent = create_agent(
    model=llm,
    tools=[_hybrid_search, fts_search, query_documents],
    system_prompt=system_prompt
)

def query_rag(user_query: str):
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": user_query}
        ]
    })

    return response
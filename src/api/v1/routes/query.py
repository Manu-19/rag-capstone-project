import json
from fastapi import APIRouter
from src.api.v1.schemas.query_schema import QueryRequest, QueryResponse
from src.services.agent import query_rag

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query_api(request: QueryRequest):

    if not request.query or len(request.query) < 3:
        return {"error": "Invalid query"}

    result = query_rag(request.query)

    try:
        ai_msg = result["messages"][-1]

        if isinstance(ai_msg.content, list):
            raw_text = ai_msg.content[0]["text"]
        else:
            raw_text = ai_msg.content

        parsed = json.loads(raw_text)
        print(parsed)

    except Exception as e:
        print("RAW RESULT:", result)
        return {
            "query": request.query,
            "answer": "Error parsing response",
            "retrieved_content": []
        }

    return QueryResponse(
        query=parsed.get("query", request.query),
        answer=parsed.get("answer", ""),
        page_no=parsed.get("page_no", ""),
        section=parsed.get("section", ""),
        document_name = parsed.get("document_name", ""),
        retrieved_content = parsed.get("chunks", [])
    )
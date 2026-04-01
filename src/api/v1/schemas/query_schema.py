from pydantic import BaseModel
from typing import List, Any, Optional


class QueryRequest(BaseModel):
    query: str


class Citation(BaseModel):
    document_name: str
    page_no: str
    section: str


class QueryResponse(BaseModel):
    query: str
    answer: str
    page_no: str
    section: str
    document_name: str
    retrieved_content: Optional[List[str]]  =[]
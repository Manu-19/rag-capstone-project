import os 
from dotenv import load_dotenv 
from langchain_postgres import PGVector 
from langchain_google_genai import GoogleGenerativeAIEmbeddings 

load_dotenv(override=True) 

PG_CONNECTION = os.getenv("PG_CONNECTION_STRING")

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-2-preview",
        api_key=os.getenv("GOOGLE_API_KEY")
    )

def get_vector_store(collection_name: str = "loan_support_desk"):
    return PGVector(
        collection_name=collection_name,
        connection=PG_CONNECTION,
        embeddings=get_embeddings(),
        use_jsonb=True
    )
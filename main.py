import os
from typing import Type

import cohere
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from vectordb import PineconeDB, VectorDatabase, RedisDB

# Initializations
app = FastAPI()

# Initialize Cohere
co = cohere.Client(os.environ["COHERE_API_KEY"])

# Define the index name
index_name = "wikipedia-embeddings"

vector_db = None


# Define the request model
class QueryRequest(BaseModel):
    query: str


# Dependency function to choose a vector database implementation
def get_vector_db() -> Type[VectorDatabase]:
    # Choose either PineconeDatabase or QdrantDatabase here
    vector_db_class = RedisDB  # or QdrantDatabase
    return vector_db_class(index_name)


# @app.on_event("startup")
# async def startup_event():
#     vector_db = get_vector_db()
#     vector_db.upsert()


@app.post("/ask")
async def ask(
    request: QueryRequest, vector_db: VectorDatabase = Depends(get_vector_db)
) -> dict:
    # Get the embeddings
    query_embeds = co.embed([request.query], model="multilingual-22-12").embeddings

    # Query the VectorDatabase
    result = vector_db.query(query_embedding=query_embeds[0])

    return {"result": result}


# @app.post("/upsert")
# async def upsert():
#     vector_db = get_vector_db()
    return vector_db.upsert()


@app.get("/health")
async def health():
    return {"status": "ok"}


# @app.on_event("shutdown")
# async def shutdown():
#     vector_db = get_vector_db()
# #     vector_db.delete_index()

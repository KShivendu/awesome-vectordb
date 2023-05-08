import math
import os
from typing import List

import cohere
import pinecone
from datasets import load_dataset
from fastapi import FastAPI
from loguru import logger


class VectorDB:
    def __init__(self, index_name):
        self.index_name = index_name
        logger.info(f"Index name: {self.index_name} initialized")
        # Load the dataset
        large_dataset = load_dataset(
            "Cohere/wikipedia-22-12-simple-embeddings", split="train"
        )
        # We will only use the first 1000 records
        self.dataset = large_dataset[0:200]

        logger.info(f"Dataset loaded with {len(self.dataset)} records")


class PineconeDB(VectorDB):
    def __init__(self, index_name):
        super().__init__(index_name)
        pinecone.init(
            api_key=os.environ["PINECONE_API_KEY"],
            environment=os.environ["PINECONE_ENVIRONMENT"],
        )
        # Create the index if it doesn't exist
        if self.index_name not in pinecone.list_indexes():
            logger.info(f"Creating index: {self.index_name}")
            pinecone.create_index(index_name, dimension=768, metric="cosine")

        # Connect to the index
        self.index = pinecone.Index(index_name=index_name)

    def upsert(self) -> str:
        batch_size = 100  # Adjust the batch size as per your requirements
        logger.info(f"total vectors from upsert: {len(self.dataset)}")
        num_vectors = len(self.dataset)
        logger.info(f"total num of vectors from upsert: {num_vectors}")
        num_batches = math.ceil(num_vectors / batch_size)

        logger.info(f"Upserting {num_vectors} vectors in {num_batches} batches")

        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, num_vectors)

            vectors_batch = [
                (
                    f"{self.dataset[j]['id']}",
                    self.dataset[j]["emb"],
                    {"text": self.dataset[j]["text"]},
                )
                for j in range(start_idx, end_idx)
            ]

            logger.info(
                f"Upserting batch {i + 1} of {num_batches}, from {start_idx} to {end_idx}"
            )

            self.index.upsert(vectors_batch)

        logger.info(f"Upserted {num_vectors} vectors")

        return "Upserted successfully"

    def query(self, query_embedding: List[float]) -> dict:
        return self.index.query(
            vector=query_embedding,
            top_k=3,
            include_values=True,
            include_metadata=True,
        )


# Main code
app = FastAPI()
index_name = "wikipedia-embeddings"
pinecone_obj = PineconeDB(index_name)


@app.post("/upsert")
def db_upsert():
    if pinecone_obj.upsert() == "Upserted successfully":
        return "Upserted successfully"
    return "Upsert failed"


@app.post("/query")
def db_query(query: str):
    logger.info(f"Query: {query}")
    co = cohere.Client(os.environ["COHERE_API_KEY"])
    # get the embeddings
    query_embeds = co.embed([query], model="multilingual-22-12").embeddings

    return pinecone_obj.query(query_embedding=query_embeds[0])

    # Output:
    # {
    #     "matches": [
    #         {
    #             "id": "9",
    #             "metadata": {
    #                 "text": "In the Old Testament, Almighty God is the one who created the world. The God of the Old Testament is not always presented as the only God who exists Even though there may be other gods, the God of the Old Testament is always shown as the only God whom Israel is to worship. The God of the Old Testament is the one 'true God'; only Yahweh is Almighty. Both Jews and Christians have always interpreted the Bible (both the 'Old' and 'New' Testaments) as an affirmation of the oneness of Almighty God."
    #             },
    #             "score": 40.6401978,
    #             "values": [0.479291856, ..., 0.31344567],
    #         }
    #     ],
    #     "namespace": "",
    # }


if __name__ == "__main__":
    app.run()

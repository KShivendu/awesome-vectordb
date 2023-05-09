import math
import os
from typing import List

import pinecone
from datasets import load_dataset
from loguru import logger


class VectorDatabase:
    def __init__(self, index_name, top_k: int = 3):
        self.index_name = index_name
        logger.info(f"Index name: {self.index_name} initialized")
        # Load the dataset
        self.dataset = load_dataset(
            "Cohere/wikipedia-22-12-simple-embeddings", split="train"
        )
        logger.info(f"Dataset loaded with {len(self.dataset)} records")
        self.top_k = top_k

    def upsert(self) -> str:
        raise NotImplementedError

    def query(self, query_embedding: List[float]) -> dict:
        raise NotImplementedError


class PineconeDB(VectorDatabase):
    def __init__(self, index_name):
        super().__init__(index_name)
        self.batch_size = 50
        pinecone.init(
            api_key=os.environ["PINECONE_API_KEY"],
            environment=os.environ["PINECONE_ENVIRONMENT"],
        )
        # Create the index if it doesn't exist
        if self.index_name not in pinecone.list_indexes():
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
            top_k=self.top_k,
            include_values=True,
            include_metadata=True,
        )

    def delete_index(self) -> str:
        pinecone.delete_index(self.index_name)
        return "Index deleted"


# Run the FastAPI app using uvicorn (add this line in another file or in the __main__ block)
# uvicorn.run(app, host="0.0.0.0", port=8000)

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

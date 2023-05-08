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
        self.top_k = 3

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
        self.vectors = [
            (
                f"{self.dataset[i]['id']}",
                self.dataset[i]["emb"],
                {"text": self.dataset[i]["text"]},
            )
            for i in range(len(self.dataset))
        ]

        # Note: When upserting larger amounts of data, upsert data in batches
        # of 100 vectors or fewer over multiple upsert requests.

        # Upsert the vectors in batches of 50
        num_vectors = len(self.vectors)

        for i in range(0, num_vectors, self.batch_size):
            batch = self.vectors[i : i + self.batch_size]
            self.index.upsert(batch)

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

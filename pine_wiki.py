import os

import cohere
import pinecone
from datasets import load_dataset
from typing import List


class VectorDB:
    def __init__(self, index_name):
        self.index_name = index_name
        # Load the dataset
        self.dataset = load_dataset(
            "Cohere/wikipedia-22-12-simple-embeddings", split="train"
        )


class PineconeDB(VectorDB):
    def __init__(self, index_name):
        super().__init__(index_name)
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
        batch_size = 50
        num_vectors = len(self.vectors)

        for i in range(0, num_vectors, batch_size):
            batch = self.vectors[i : i + batch_size]
            self.index.upsert(batch)

        return "Upserted successfully"

    def query(self, query_embedding: List[float]) -> dict:
        return self.index.query(
            vector=query_embedding,
            top_k=3,
            include_values=True,
            include_metadata=True,
        )


# Main code
if __name__ == "__main__":
    # Step 1: Create an index in Pinecone
    # Define the index name
    index_name = "wikipedia-embeddings"

    co = cohere.Client(os.environ["COHERE_API_KEY"])

    # get the embeddings
    query = "What is Old Testament?"
    query_embeds = co.embed([query], model="multilingual-22-12").embeddings

    # Initialize the PineconeDB
    pinecone_obj = PineconeDB(index_name)
    pinecone_obj.upsert()

    result = pinecone_obj.query(query_embedding=query_embeds[0])

    print(result)
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

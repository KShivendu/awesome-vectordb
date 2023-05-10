import math
import os
from typing import List

import pinecone
from datasets import load_dataset
from loguru import logger
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import CollectionStatus, PointStruct, UpdateStatus


class VectorDatabase:
    """VectorDatabase class initializes the Vector Database index_name and loads the dataset
    for the usage of the subclasses."""

    def __init__(self, index_name, top_k: int = 3):
        self.index_name = index_name
        logger.info(f"Index name: {self.index_name} initialized")
        # Load the dataset
        self.dataset = load_dataset(
            "Cohere/wikipedia-22-12-simple-embeddings", split="train"
        )
        logger.info(f"Dataset loaded with {len(self.dataset)} records")
        self.top_k = top_k
        self.dimension = 768

    def upsert(self) -> str:
        raise NotImplementedError

    def query(self, query_embedding: List[float]) -> dict:
        raise NotImplementedError


class PineconeDB(VectorDatabase):
    """PineconeDB class is a subclass of VectorDatabase that
    interacts with the Pinecone Cloud Vector Database index and
    has the following methods:
    - upsert: Upserts the embedding into the Pinecone index along with the metadata
    - query: Queries the Pinecone index with the query embedding along with the metadata
    - delete_index: Deletes the Pinecone index
    """

    def __init__(self, index_name):
        super().__init__(index_name)
        self.batch_size = 100  # Adjust the batch size as per your requirements
        pinecone.init(
            api_key=os.environ["PINECONE_API_KEY"],
            environment=os.environ["PINECONE_ENVIRONMENT"],
        )
        # Create the index if it doesn't exist
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(index_name, dimension=self.dimension, metric="cosine")

        # Connect to the index
        self.index = pinecone.Index(index_name=index_name)

    def upsert(self) -> str:
        logger.info(f"total vectors from upsert: {len(self.dataset)}")
        num_vectors = len(self.dataset)
        logger.info(f"total num of vectors from upsert: {num_vectors}")
        num_batches = math.ceil(num_vectors / self.batch_size)

        logger.info(f"Upserting {num_vectors} vectors in {num_batches} batches")

        for i in range(num_batches):
            start_idx = i * self.batch_size
            end_idx = min((i + 1) * self.batch_size, num_vectors)

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
        # Pinecone Output:
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
        return self.index.query(
            vector=query_embedding,
            top_k=self.top_k,
            include_values=True,
            include_metadata=True,
        )

    def delete_index(self) -> str:
        pinecone.delete_index(self.index_name)
        return "Index deleted"


class QdrantDB(VectorDatabase):
    """QdrantDB class is a subclass of VectorDatabase that
    interacts with the Qdrant Cloud Vector Database. It has the following methods:
    - upsert: Upserts the dataset into the Qdrant collection(index) with the payload(metadata)
    - query: Queries the Qdrant collection(index) with the query embedding along with
    the payload(metadata)
    - delete_index: Deletes the Qdrant collection(index)
    """

    def __init__(self, index_name):
        super().__init__(index_name)
        self.batch_size = 1000  # Adjust the batch size as per your requirements

        self.qdrant_client = QdrantClient(
            os.environ["QDRANT_URL"],
            prefer_grpc=True,
            api_key=os.environ["QDRANT_API_KEY"],
        )

        collection_info = self.qdrant_client.get_collection(
            collection_name=self.index_name
        )

        # Create the collection(index) if it doesn't exist
        if collection_info.status != CollectionStatus.GREEN:
            self.qdrant_client.recreate_collection(
                collection_name=self.index_name,
                vectors_config=models.VectorParams(
                    size=self.dimension, distance=models.Distance.COSINE
                ),
            )

    def upsert(self) -> str:
        logger.info(f"total vectors from upsert: {len(self.dataset)}")
        num_vectors = len(self.dataset)
        logger.info(f"total num of vectors from upsert: {num_vectors}")
        num_batches = math.ceil(num_vectors / self.batch_size)

        logger.info(f"Upserting {num_vectors} vectors in {num_batches} batches")

        for i in range(num_batches):
            start_idx = i * self.batch_size
            end_idx = min((i + 1) * self.batch_size, num_vectors)

            vectors_batch = [
                PointStruct(
                    id=self.dataset[j]["id"],
                    vector=self.dataset[j]["emb"],
                    payload={"text": self.dataset[j]["text"]},
                )
                for j in range(start_idx, end_idx)
            ]

            logger.info(
                f"Upserting batch {i + 1} of {num_batches}, from {start_idx} to {end_idx}"
            )

            operation_info = self.qdrant_client.upsert(
                collection_name=self.index_name, wait=True, points=vectors_batch
            )

            if operation_info.status != UpdateStatus.COMPLETED:
                raise Exception("Upsert failed")

        logger.info(f"Upserted {num_vectors} vectors")

        return "Upserted successfully"

    def query(self, query_embedding: List[float]) -> dict:
        # Qdrant Output:
        # {
        #     "result": [
        #         {"id": 4, "score": 1.362},
        #         {"id": 1, "score": 1.273},
        #         {"id": 3, "score": 1.208},
        #     ],
        #     "status": "ok",
        #     "time": 0.000055785,
        # }
        return self.qdrant_client.search(
            collection_name=self.index_name,
            query_vector=query_embedding,
            limit=self.top_k,
            with_payload=True,
        )

    def delete_index(self) -> str:
        self.qdrant_client.delete_collection(collection_name=self.index_name)
        return "Index deleted"

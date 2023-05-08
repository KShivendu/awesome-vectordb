import os

import cohere
import pinecone
from datasets import load_dataset

pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT"],
)

# List the indexes
pinecone_indexes = pinecone.list_indexes()


# Step 1: Create an index in Pinecone
# Define the index name
index_name = "wikipedia-embeddings"

# Create the index if it doesn't exist
if index_name not in pinecone_indexes:
    pinecone.create_index(index_name, dimension=768, metric="euclidean")


# Step 2: Add embeddings to the index

# Load the dataset
dataset = load_dataset("Cohere/wikipedia-22-12-simple-embeddings", split="train")

# Connect to the index
index = pinecone.Index(index_name=index_name)

# Vector Sample
# vectors = [
#         (
#          "vec1",                # Vector ID
#          [0.1, 0.2, 0.3, 0.4],  # Dense vector values
#          {"genre": "drama"}     # Vector metadata
#         ),
#         (
#          "vec2",
#          [0.2, 0.3, 0.4, 0.5],
#          {"genre": "action"}
#         )
#     ],

# Build a list of vectors to upsert
vectors = []

for i in range(10):
    vectors.append(
        (
            f"{dataset[i]['id']}",
            dataset[i]["emb"],
            {"text": dataset[i]["text"]},
        )
    )

print(vectors)

# Upsert the vectors

# Note: When upserting larger amounts of data, upsert data in batches
# of 100 vectors or fewer over multiple upsert requests.
index.upsert(vectors)

# Step 3: Query the index
co = cohere.Client(os.environ["COHERE_API_KEY"])

# get the embeddings
query = "What is Old Testament?"
query_embeds = co.embed([query], model="multilingual-22-12").embeddings

result = index.query(
    vector=query_embeds[0],
    top_k=3,
    include_values=True,
    include_metadata=True,
)

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

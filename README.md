# Awesome VectorDB

Everything you need to decide and work with VectorDBs aka Vector Databases, Vector Search Engines

# A Comparative Overview of Vector Databases

When dealing with high-dimensional data or working on tasks such as similarity search, recommendation systems, and so on, vector databases (also known as vector search engines) can come in quite handy. These databases are optimized to handle vector data, enabling efficient storage, updates, and retrieval of vectors.

In this post, we'll explore and compare six popular vector management tools: Pinecone, Qdrant, Weaviate, FAISS, PG Vector, and Redis. Let's dive in!

## Pinecone
Pinecone is a vector database that excels in being web-dev friendly. While it's not primarily designed for text management, it can handle embeddings quite well. However, any text data can be converted to embeddings when sent to Pinecone. The primary query payload Pinecone handles is embeddings. As for the source code, it's closed, which might be a limitation for those seeking customization, privacy or transparency.

## Qdrant
Qdrant is an open-source vector database with support for updates and text management using payloads. It can handle a variety of query payloads, including text, embeddings, geospatial information and other data types that fit into the payload structure. This makes Qdrant a flexible and powerful option for different use cases. You do have to make the embeddings externally and insert/upsert though.

## Weaviate
Weaviate is another open-source vector database. I didn't quite understand it's update capabilities clearly. It provides some text management and also offers schemas to define structure. Weaviate can handle a diverse set of query payloads, including text, embeddings, and any other data as a blob. This level of versatility makes Weaviate suitable for a wide range of applications.

## FAISS
FAISS (Facebook AI Similarity Search) is a library developed by Facebook AI that excels in efficient similarity search and clustering of high-dimensional vectors. Its update capabilities vary based on the type of index used - while flat indices don't support updates, IVF indices do. FAISS is not designed for text management and requires external handling of text data. It predominantly deals with embeddings as a query payload. Being an open-source library, FAISS offers the opportunity for customization and detailed understanding of its internals. It is also NOT a database. 

## PG Vector
PG Vector is an extension to PostgreSQL, offering vector support to this popular relational database. It supports updates and handles text as part of its PostgreSQL core functionalities. However, when it comes to query payloads, PG Vector is predominantly designed for embeddings. Other data types need to be managed like standard PostgreSQL data. Being an open-source extension, it allows customization and thorough inspection of the source code. [Benchmarks](https://ann-benchmarks.com/pgvector.html) indicate this is quite slow for more than 10 queries per second. 

## Redis
Redis is a popular in-memory data structure store used as a database, cache, and message broker. The vector support comes from its modules, which are open source even though the core Redis stack is closed source. It's unclear whether Redis supports updates in the context of vector data. It does provide text management capabilities through metadata. Like Qdrant and Weaviate, Redis can handle a wide variety of data types as query payloads, including text and embeddings.

This post provides a high-level comparison of these databases, but I encourage you to explore each one in more depth to make an informed decision. As always, the best tool is the one that works best for you!

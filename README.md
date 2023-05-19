# Awesome VectorDB

Everything you need to decide and work with VectorDBs aka Vector Databases, Vector Search Engines

# A Comparative Overview of Vector Databases

When dealing with high-dimensional data or working on tasks such as similarity search, recommendation systems, and so on, vector databases (also known as vector search engines) can come in quite handy. These databases are optimized to handle vector data, enabling efficient storage, updates, and retrieval of vectors.

Points to cover:

1. Security 
2. Streaming index option 
3. Updates
4. Payload Management
5. Cost: is actually different heads: Pricing e.g. GB vs flat
6. Performance - latency, throughput, RAM and CPU usage — this is the interesting part and where we started from.

In this post, we'll explore and compare six popular vector management tools: Pinecone, Qdrant, Weaviate, FAISS, PG Vector, and Redis. Let's dive in!

## Pinecone
Pinecone is a vector database that excels in being web-dev friendly. While it's not primarily designed for text management, it can handle embeddings quite well. However, any text data can be converted to embeddings when sent to Pinecone. The primary query payload Pinecone handles is embeddings. As for the source code, it's closed, which might be a limitation for those seeking customization, privacy or transparency.

1. Security: To use Pinecone, you'd need an API key and an environment value. Environment value is the Cloud region where your data is stored.
2. Streaming index option: Pinecone does not support streaming indexes.
3. Updates: Pinecone supports updates.
4. Payload Management: Pinecone can handle embeddings and text. But there's a catch with respect to the text. The text can be stored as a metadata field with each vector in an index, as key-value pairs in a JSON object but is limited to a size of 40kb. If you want to store more text, you'd have to store it in a separate database and use the vector ID as a key to retrieve the text.
5. Pricing: Pinecone's pricing can be split into three parts(or pods as pinecone calls it): s1 - storage optimized, p1 - performance optimized and p2 - 2nd gen performance. So, if you'd require to store more vectors, you'd have to go for s1. If you'd require more throughput, you'd have to go for p1 or p2. The pricing is based on the number of vectors. It's a pay-as-you-go model based on the hours and the number of pods you require. You can find more details [here](https://www.pinecone.io/pricing/).
6. Performance: *Pinecone is quite fast. It's latency is in the range of 10-20ms. It's throughput is in the range of 1000-2000 queries per second. It's RAM usage is in the range of 1-2GB and CPU usage is in the range of 0.1-0.2 cores.* <- Change this.
7. Developer Experience: The only issue with Pinecone is that the api specifically asks us to throttle our upserts to about 100 vectors per batch - which delays things. But they do offer an alternative solution with using grpc and streaming upserts. But that's a bit more work. You can read more about it [here](https://docs.pinecone.io/docs/performance-tuning).

## Qdrant
Qdrant is an open-source vector database with support for updates and text management using payloads. It can handle a variety of query payloads, including text, embeddings, geospatial information and other data types that fit into the payload structure. This makes Qdrant a flexible and powerful option for different use cases. You do have to make the embeddings externally and insert/upsert though.

1. Security: As Qdrant is open-source, it comes in two flavors: One where you can run locally and one that is hosted on the cloud. The local version can be run using a pre-built docker image. The cloud version is hosted only on AWS(while in they're in beta). The cloud version comes with and api key and a path to the cloud instance for every cluster. Also, there is a mechanism to have one api key to access all the clusters - if you're keen on central management etc. *The local version does not require any authentication.*??
2. Streaming index option: Qdrant does not support streaming indexes.
3. Updates: Qdrant supports updates.
4. Payload Management: Qdrant allows you to store any information along with the vector as a JSON payload. Additionally, you can also opt to do an indexing on payloads for better filtering and querying. You can read more about it [here](https://qdrant.tech/documentation/payload/#payload-indexing).
5. Pricing: Qdrant is open-source. So, it's free to use. But if you'd like to use the cloud version, you'd have to pay for their managed instance. You can find more details [here](https://qdrant.tech/pricing/). The balancing act here w.r.t pricing is how you'd like some of your data(vector or payload) to be stored and persisted. Whether In-memory or on disk or a hybrid of these two. You can read more about it [here](https://qdrant.tech/documentation/storage/). PS: The In-memory option pricing might get a little steep if you have a lot of data.
6. Performance: *Qdrant is quite fast. It's latency is in the range of 10-20ms. It's throughput is in the range of 1000-2000 queries per second. It's RAM usage is in the range of 1-2GB and CPU usage is in the range of 0.1-0.2 cores.* <- Change this.
7. Develoeper Experience: It's in a very nascent stage imho as some of the error messages we faced 
while using the cloud variant weren't even related to the actual issue. 

## Weaviate
Weaviate is another open-source vector database. I didn't quite understand it's update capabilities clearly. It provides some text management and also offers schemas to define structure. Weaviate can handle a diverse set of query payloads, including text, embeddings, and any other data as a blob. This level of versatility makes Weaviate suitable for a wide range of applications.

1. Security: Weaviate is open-source. So, it comes in two flavors: One where you can run locally and one that is hosted on the cloud. The local version can be run using a pre-built docker image. There are two methods available for authentication. 1. Via the API key and 2. Via OIDC authentication (WCS username & password). The recommended method is to use the API key. You can also choose to not have an authentication method but that's not recommended. You can read more about it [here](https://weaviate.io/developers/weaviate/quickstart/connect#overview).
2. Streaming index option: Weaviate does support streaming indexes via their Graphql API.
3. Updates: Weaviate supports updates.
4. Payload Management: Weaviate allows you to store any information based on the class and it's respective schema(data structure of your data) you define. You can read more about it [here](https://weaviate.io/developers/weaviate/configuration/schema-configuration). That said, there is also an automatic schema detection and creation option available in Weaviate. But if you're sure about what kind of data you're going to store, it's better to define the schema yourself.
5. Pricing: Weaviate is open-source. So, it's free to use. But if you'd like to use the cloud version, you'd have to pay for their managed instance or can use a hybrid option where you bring their database to your vpc/infrastructure. You can find more details [here](https://weaviate.io/pricing/). The pricing is pretty straightforward with you paying for the number of objects you store and the number of queries you make apart from the SLA tier you choose based on the criticality of your business.
6. Performance: *Weaviate is quite fast. It's latency is in the range of 10-20ms. It's throughput is in the range of 1000-2000 queries per second. It's RAM usage is in the range of 1-2GB and CPU usage is in the range of 0.1-0.2 cores.* <- Change this.
7. Developer Experience: It took up some time in defining the schema and understanding the data structure. But once that was done, it was pretty straightforward to use.

## FAISS
FAISS (Facebook AI Similarity Search) is a library developed by Facebook AI that excels in efficient similarity search and clustering of high-dimensional vectors. Its update capabilities vary based on the type of index used - while flat indices don't support updates, IVF indices do. FAISS is not designed for text management and requires external handling of text data. It predominantly deals with embeddings as a query payload. Being an open-source library, FAISS offers the opportunity for customization and detailed understanding of its internals. It is also NOT a database. 

1. Security: FAISS is open-source and can only be run locally. So, there is no security mechanism available.
2. Streaming index option: FAISS does not support streaming indexes.
3. Updates: FAISS CPU does not support updates. But FAISS GPU does support updates with an IVF Index.
4. Payload Management: FAISS does not support payload management. You'd need to handle it externally, mostly in tandem with a pickled file.
5. Pricing: FAISS is open-source. So, it's free to use.
6. Performance: *FAISS is quite fast. It's latency is in the range of 10-20ms. It's throughput is in the range of 1000-2000 queries per second. It's RAM usage is in the range of 1-2GB and CPU usage is in the range of 0.1-0.2 cores.* <- Change this.
7. Developer Experience: With no update support and no payload management with the CPU version, the learning curve to some, might be a little steep. But with a very low memory footprint and a very high throughput, it's a great option for a lot of use cases.


## PG Vector
PG Vector is an extension to PostgreSQL, offering vector support to this popular relational database. It supports updates and handles text as part of its PostgreSQL core functionalities. However, when it comes to query payloads, PG Vector is predominantly designed for embeddings. Other data types need to be managed like standard PostgreSQL data. Being an open-source extension, it allows customization and thorough inspection of the source code. [Benchmarks](https://ann-benchmarks.com/pgvector.html) indicate this is quite slow for more than 10 queries per second. 

1. Security: As PG vector is an extension to PostgreSQL, it inherits the security mechanisms of PostgreSQL. 
2. Streaming index option: PG Vector does not support streaming indexes.
3. Updates: PG Vector supports updates.
4. Payload Management: As PG Vector is an extension to PostgreSQL, it just supports embeddings as a query payload. Other data types need to be managed like standard PostgreSQL data.
5. Pricing: PG Vector is open-source. So, it's free to use. 
6. Performance: *PG Vector is quite fast. It's latency is in the range of 10-20ms. It's throughput is in the range of 1000-2000 queries per second. It's RAM usage is in the range of 1-2GB and CPU usage is in the range of 0.1-0.2 cores.* <- Change this.
7. Developer Experience: Contrary to most vector databases, as PG Vector is an extension to PostgreSQL, the way to think about data management is very similar to how you'd think about data management in any relational database. So, the learning curve is not that steep. It is one of the most sought after vector database options requested by the dev community to be added to the existing database options by a lot of cloud providers.



## Redis
Redis is a popular in-memory data structure store used as a database, cache, and message broker. The vector support comes from its modules, which are open source even though the core Redis stack is closed source. It's unclear whether Redis supports updates in the context of vector data. It does provide text management capabilities through metadata. Like Qdrant and Weaviate, Redis can handle a wide variety of data types as query payloads, including text and embeddings.

This post provides a high-level comparison of these databases, but I encourage you to explore each one in more depth to make an informed decision. As always, the best tool is the one that works best for you!

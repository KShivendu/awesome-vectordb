# The Ultimate Guide to VectorDB

Your one-stop resource for decision-making and working with VectorDBs aka Vector Databases, Vector Search Engines

# A Comparative Overview of Vector Databases

When dealing with high-dimensional data or working on tasks such as similarity search, recommendation systems, and so on, vector databases (also known as vector search engines) are essential. These databases are optimized to handle vector data, enabling efficient storage, updates, and retrieval of vectors.

We'll be focusing on:

1. Security 
2. Streaming index options
3. Updates
4. Payload Management
5. Cost: Various pricing models e.g., GB vs flat
6. Performance - latency, throughput, RAM, and CPU usage — this is the interesting part and where we started from.

In this post, we'll explore and compare six popular vector management tools: Pinecone, Qdrant, Weaviate, FAISS, PG Vector, and Redis. Let's dive in!

## Pinecone
Pinecone is a vector database that stands out for being web-dev friendly. While it's not primarily designed for text management, it can handle embeddings quite well. However, any text data can be converted to embeddings when sent to Pinecone. The primary query payload Pinecone handles is embeddings. As for the source code, it's closed, which might be a limitation for those seeking customization, privacy, or transparency.

1. Security: To use Pinecone, you need an API key and an environment value. The environment value refers to the Cloud region where your data is stored.
2. Streaming index option: Pinecone does not support streaming indexes.
3. Updates: Pinecone supports updates.
4. Payload Management: Pinecone can handle embeddings and text. However, the text can be stored as a metadata field with each vector in an index, as key-value pairs in a JSON object but is limited to a size of 40kb. If you want to store more text, you will have to store it in a separate database and use the vector ID as a key to retrieve the text.
5. Pricing: Pinecone's pricing can be split into three parts (or pods as Pinecone calls them): s1 - storage optimized, p1 - performance optimized, and p2 - 2nd gen performance. So, if you require more storage, you should go for s1. If you require more throughput, you should opt for p1 or p2. The pricing is based on the number of vectors. It's a pay-as-you-go model based on the hours and the number of pods you require. You can find more details [here](https://www.pinecone.io/pricing/).
6. Performance: *TK Please update this with the actual performance metrics.*
7. Developer Experience: The only issue with Pinecone is that the API specifically asks us to throttle our upserts to about 100 vectors per batch, which can delay processes. However, they do offer an alternative solution using gRPC and streaming upserts, which is a bit more work. You can read more about it [here](https://docs.pinecone.io/docs/performance-tuning).

## Qdrant
Qdrant is a versatile open-source vector database written in Rust, it's a performance first view of the tooling. It handles various query payloads, such as text, embeddings, geospatial information, and other data types compatible with the payload structure. This versatility makes Qdrant a robust and adaptable choice for diverse use cases. However, you must create embeddings externally before insertion or upsertion.

1. Security: Qdrant offers two versions: a local version that can be run using a pre-built Docker image, and a cloud-hosted version available only on AWS (during the beta phase). The cloud version provides an API key and a path to the cloud instance for each cluster. For centralized management, there's an option to use one API key to access all clusters. The local version, however, does not require any authentication.
2. Streaming index option: Qdrant does not currently support streaming indexes.
3. Updates: Qdrant fully supports updates.
4. Payload Management: Qdrant empowers you to store any accompanying information as a JSON payload with the vector. There's also an option to index payloads for improved filtering and querying capabilities. You can read more about this [here](https://qdrant.tech/documentation/payload/#payload-indexing).
5. Pricing: As an open-source tool, Qdrant is free. However, for utilizing the cloud version, you'll need to pay for their managed instance. More details are available [here](https://qdrant.tech/pricing/). A crucial aspect to consider when it comes to pricing is the mode of data (vector or payload) storage and persistence—whether in-memory, on disk, or a hybrid of both. More on this can be found [here](https://qdrant.tech/documentation/storage/). Note: In-memory option pricing could escalate with large volumes of data.
6. Performance: *TK Kindly provide the precise performance metrics for Qdrant.*
7. Developer Experience: Qdrant is still in its early stages, which may account for occasional confusion, like the instance of receiving unrelated error messages while using the cloud variant. Nonetheless, the continuous updates and the supportive community are addressing these issues proactively. The upsert or insert limits are not enforced on the client. The `gRPC` mode is easy to setup for higher throughput.

## Weaviate
Weaviate is an open-source vector database with robust capabilities for handling diverse query payloads, including text, embeddings, and any other data as a blob. It also offers schemas to define structure, which significantly adds to its adaptability across different applications. However, its update capabilities could be more clearly defined.

1. Security: Weaviate can be run both locally using a pre-built Docker image and hosted on the cloud. Two authentication methods are available: 1. Via the API key, and 2. Via OIDC authentication (WCS username & password), with the API key being the recommended method. While it's possible to opt out of authentication, it's not advised due to potential security risks. More details on this can be found [here](https://weaviate.io/developers/weaviate/quickstart/connect#overview).
2. Streaming index option: Weaviate supports streaming indexes through their GraphQL API.
3. Updates: Weaviate supports updates.
4. Payload Management: Weaviate enables you to store any information based on the class and the corresponding schema you define. You can learn more about this [here](https://weaviate.io/developers/weaviate/configuration/schema-configuration). It's worth noting that Weaviate offers automatic schema detection and creation, although manually defining the schema might be advisable if you have a clear understanding of the data to be stored.
5. Pricing: Being open-source, Weaviate is free. However, if you wish to use the cloud version, you'll need to pay for their managed instance or opt for a hybrid approach where you bring their database to your VPC/infrastructure. Detailed pricing information is available [here](https://weaviate.io/pricing/). Pricing is straightforward, dependent on the number of stored objects, the number of queries you make, and the chosen SLA tier based on the criticality of your business.
6. Performance: *Kindly provide the precise performance metrics for Weaviate.*
7. Developer Experience: Initial stages of schema definition and understanding the data structure can take some time. However, once familiarized with this process, Weaviate becomes quite straightforward to use.

## FAISS
FAISS (Facebook AI Similarity Search) is a highly efficient library developed by Facebook AI for similarity search and clustering of high-dimensional vectors. Its capacity for updates depends on the index type in use - flat indices do not support updates, while IVF indices do. FAISS, not being a database, is focused primarily on embeddings and does not offer text management, necessitating external handling of text data. As an open-source library, it provides opportunities for customization and in-depth exploration of its internal workings.

1. Security: Being open-source and designed to run only locally, FAISS does not come with a built-in security mechanism.
2. Streaming index option: FAISS does not support streaming indexes.
3. Updates: Updates are unsupported by FAISS CPU, but FAISS GPU does support updates with an IVF Index.
4. Payload Management: FAISS lacks payload management support, hence it requires external handling, often using a pickled file.
5. Pricing: As an open-source library, FAISS is free to use.
6. Performance: *Kindly provide specific performance metrics for FAISS.*
7. Developer Experience: Despite the lack of update support and payload management in the CPU version, which may steepen the learning curve for some users, FAISS offers a low memory footprint and high throughput, making it a valuable choice for many use cases.

## PG Vector
PG Vector is an extension for PostgreSQL that introduces vector support to this widely used relational database. It allows for updates and provides text management as a core functionality of PostgreSQL. Regarding query payloads, PG Vector is primarily geared towards embeddings, with other data types requiring standard PostgreSQL data management. Being open-source, it allows for customization and comprehensive inspection of the source code. [Benchmarks](https://ann-benchmarks.com/pgvector.html) suggest that it may perform slowly when handling more than 10 queries per second.

1. Security: PG Vector, being an extension of PostgreSQL, inherits PostgreSQL's security mechanisms.
2. Streaming index option: PG Vector does not support streaming indexes.
3. Updates: PG Vector does support updates.
4. Payload Management: PG Vector, as an extension of PostgreSQL, supports embeddings as a query payload. For other data types, they need to be managed as standard PostgreSQL data.
5. Pricing: Being an open-source extension, PG Vector is free to use.
6. Performance: *Please provide accurate performance metrics for PG Vector.*
7. Developer Experience: In contrast to most vector databases, PG Vector's similarity to PostgreSQL in data management means a less steep learning curve. It's one of the most requested vector database options to be included by the developer community in the offerings of various cloud providers.

## Redis
Redis, a widely used in-memory data structure store, serves as a database, cache, and message broker. Vector support is provided through its modules, which remain open source despite the core Redis stack being closed source. It's unclear whether Redis supports updates when dealing with vector data. However, it does offer text management capabilities through metadata and, like Qdrant and Weaviate, can handle a broad range of data types as query payloads, including text and embeddings.

# Optimizing Vector Databases: Tricks and Best Practices

## Querying in Vector Databases
* Understanding the Querying Process
* Types of Queries: Similarity Search, k-NN, Range Search e.g. Grouped Documents, Metadata filtering
* Query Optimization: Choosing the Right Index, Balancing Precision and Speed, Cost and throughput
* Real-World Query Examples and How to Handle Them

## Performance Optimization
* Understanding Performance Metrics in Vector Space
* Storage Optimization: Efficient Disk Usage, Reducing I/O Overhead
* Load Balancing and Sharding: Distributing Data and Workload
* Hardware Considerations: Effect of Memory and CPU on Performance
* Benchmarking and Monitoring: Tools and Techniques for Performance Tracking

## Security Considerations
* Data Encryption: Ensuring Data At Rest Security
* Access Control: Managing User Permissions and Roles
* Audit Logging: Tracking Data Access and Modifications
* Securing Data Transfers: SSL/TLS, gRPC Security Features

## Maintaining and Scaling Vector Databases
* Routine Maintenance: Cleanup, Defragmentation, Periodic Re-indexing
* Troubleshooting Common Issues: Performance Degradation, Failed Queries
* Scalability Strategies: Scaling Up vs Scaling Out
* Monitoring System Health: Keeping Track of System Metrics
* Backup and Disaster Recovery: Best Practices for Data Safety

## Additional Best Practices
* Effective Use of gRPC: Optimizing Data Exchange and Communication
* Advanced Search Techniques: Multimodal, Hybrid Search
* Utilizing Payloads and Filters: Advanced Data Manipulation Techniques
* Indexing Techniques: Choosing the Right Algorithm, Delayed Indexing
* Understanding and Mitigating the "Curse of Dimensionality"

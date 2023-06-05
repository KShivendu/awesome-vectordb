# Optimizing Vector Databases: Tricks and Best Practices

## Querying in Vector Databases
* Understanding the Querying Process

These are the steps that you need to follow to query a vector database:
1. Generating Embeddings: Convert your raw data, text or media, into vectors using ML algorithms or models.
2. Indexing: Upsert the vectors into the database and build your collection. All vectors of a collection must have the same dimensionality.
3. Querying: Convert your raw query, text or media, into a vector using the same ML model. Then pass it to the database along with any metadata filters you want to apply to limit the search space and get the results.

* Types of Queries: Similarity Search, k-NN, Range Search e.g. Grouped Documents, Metadata filtering

1. Similarity Search: It is performed by approximation nearest neighbours algorithms like HNSW, NMSLIB, etc.
2. Metadata Filtering: This is traditional search on the metadata that you ingest along with the embeddings. You can do all kinds of filtering on the metadata: range queries, exact match, full text search, etc dependending on what the database supports.
3. Recommendations: You can build a simple recommendation system based on this formula: `average_vector = avg(liked_vectors) + ( avg(liked_vectors) - avg(disliked_vectors) )` and then search for the average vector. Qdrant even provides an API for this out of the box.
4. Hybrid sparse-dense search: You can use two different ML models: one with a dense vector that represents the semantic meaning of your data and another with a sparse vector where each dimension of the vector represents some attribute of the data and most of the positions are 0. This also allows you to weight certain parts of the query more than others. At the moment, this is only supported by p1 and s1 pods of Pinecone.

* Query Optimization: Choosing the Right Index, Balancing Precision and Speed, Cost and throughput


Qdrant params:
- Quantization: in-memory quantization, with on-disk original vectors
- HNSW config: m and ef construct
- Optimizer params:

Pinecone params:
- Pod type: https://docs.pinecone.io/docs/indexes#p1-pods https://docs.pinecone.io/docs/choosing-index-type-and-size
- Distance metric: Eucledian, Cosine, and Dot product
- Pod size: x1, x2, x4, and x8. Every step up in size doubles the storage as well as compute capacity of the pod.

Here's a comparison of the different pod types in Pinecone with 1M vectors of 768 dimensions:

| Model |  QPS (Top_k=10) |   QPS (Top_k=250) | QPS (Top_k=1000) |                          Remarks                                       |
|-------|-----------------|-------------------|------------------|------------------------------------------------------------------------|
| p1    |      ~30        |        25         |       20         |             Ideal for low latency requirements                         |
| p2    |     ~150        |        50         |       20         |     Highest QPS and lowest latency but data ingestion is slower than p1 and drop with # of dims. |
| s1    |      ~10        |        25         |       20         | Ideal for large indexes with moderate latency requirements since it can hold 5x more indices   |


TODO: Qdrant has many params but pinecone has a few (mainly pod type). It would be great this guide gives Qdrant configs that perform similar to pod types param of Pinecone

* Real-World Query Examples and How to Handle Them

TODO


## Performance Optimization
* Understanding Performance Metrics in Vector Space
- QPS: Queries per second. Higher is better.
- Latency (p99 and p95): p99 is the 99th percentile of the latency. Lower is better.
- Indexing time: Time taken to index vectors. Lower is better.

* Storage Optimization: Efficient Disk Usage, Reducing I/O Overhead

Qdrant:
- https://qdrant.tech/articles/scalar-quantization/
- https://qdrant.tech/articles/product-quantization/


* Load Balancing and Sharding: Distributing Data and Workload
-

* Hardware Considerations: Effect of Memory and CPU on Performance
-

* Benchmarking and Monitoring: Tools and Techniques for Performance Tracking
-

* Network Optimization: Reducing network latency and using gRPC instead of REST
-

* How QPS changes with the number of vectors in the database
-

## Security Considerations
* Data Encryption: Ensuring Data At Rest Security
1. Pinecone: They provide encryption at rest for their enterprise customers. https://www.pinecone.io/security/
2. Qdrant: No information found so far in the docs. Should skim the code once.

* Access Control: Managing User Permissions and Roles
- Pinecone: Somewhat limited to mainly two types of roles: Owner and Member on both [organisation](https://docs.pinecone.io/docs/organizations#organization-roles) and [project](https://docs.pinecone.io/docs/projects#project-roles) level.
- Qdrant: No access control so far.

* Audit Logging: Tracking Data Access and Modifications
- Pinecone: AWS CloudTrail is enabled for audit logging for enterprise customers. https://www.pinecone.io/security/
- Qdrant: Not implemented so far.

* Securing Data Transfers: SSL/TLS, gRPC Security Features
1. Qdrant:
    - SSL/TLS: Supported by Qdrant
    - gRPC: Can be enabled in Qdrant using.
    ```yaml
    service:
        grpc_port: 6334
    ```

2. Pinecone:
    - SSL/TLS: Pinecone is served over HTTPS so all data transfers are encrypted by default. They encrypt data in transit. https://www.pinecone.io/security/
    - gRPC: Supported by the python SDK. You can use `index = pinecone.GRPCIndex("index-name")` to connect to the index using gRPC.

## Maintaining and Scaling Vector Databases
* Troubleshooting Common Issues: Performance Degradation, Failed Queries
- Qdrant: Expand from [Docs](https://qdrant.tech/documentation/tutorials/how-to/?selector=aHRtbCA%2BIGJvZHkgPiBkaXY6bnRoLW9mLXR5cGUoMSkgPiBzZWN0aW9uID4gZGl2ID4gZGl2ID4gZGl2ID4gYXJ0aWNsZSA%2BIGgyOm50aC1vZi10eXBlKDIp#solve-some-common-errors)

* Scalability Strategies: Scaling Up vs Scaling Out

1. Qdrant:
- Memory estimation: Rough formula `memory_size = number_of_vectors * vector_dimension * 4 bytes * 1.5`. Extra 50% is needed for metadata (indexes, point versions, etc.) as well as for temporary segments constructed during the optimization process. If you need to have payloads along with the vectors, it is recommended to store it on the disc, and only keep indexed fields in RAM.
- If you want to optimize for storage: Configure mmap storage. In this case vectors will be stored on the disc in memory-mapped files, and only the most frequently used vectors will be kept in RAM.
- Start with a simple 2GB RAM instance and you can easily scale it till 64GB before even considering horizontal scaling. In order to avoid downtime during upgrades, you can use data replication feature to migrate all the data to new node before forwarding the traffic.
- Once you need to use horizontal scaling, you'll have to choose number of shards for the collection.

* Monitoring System Health: Keeping Track of System Metrics
- Qdrant: Exposes metrics in prometheus format at /metrics endpoint
- Pinecone: Exposes metrics in prometheus format at `https://metrics.YOUR_ENVIRONMENT.pinecone.io/metrics` endpoint

* Backup and Disaster Recovery: Best Practices for Data Safety
1. Qdrant
- Qdrant OSS: Expand from [Docs](https://qdrant.tech/documentation/concepts/snapshots/#snapshots-for-the-whole-storage)
- Qdrant Cloud: https://qdrant.tech/documentation/cloud/backups/#self-service-backups
- Lastly, you can create qdrant collections from existing collections using the `init_from` param

2. Pinecone
- Create collection (static copy of your index that only consumes storage) for your index. Expand from [Docs](https://docs.pinecone.io/docs/back-up-indexes#create-a-backup-using-a-collection)

Note that you should also backup the original raw data from which you generated the embeddings. This also gives you freedom to switch to another vector database if you want to.

## Additional Best Practices
* Effective Use of gRPC: Optimizing Data Exchange and Communication
* Advanced Search Techniques: Multimodal, Hybrid Search
* Utilizing Payloads and Filters: Advanced Data Manipulation Techniques
* Indexing Techniques: Choosing the Right Algorithm, Delayed Indexing
* Understanding and Mitigating the "Curse of Dimensionality"


TODO: Maybe add a section on different approaches for multi tenancy like namespaces, metadata filtering, and seperating collections can affect performance? https://docs.pinecone.io/docs/multitenancy

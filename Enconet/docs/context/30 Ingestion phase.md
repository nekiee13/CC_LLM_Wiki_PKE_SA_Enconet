First uniqness of current project (3rd project, Supplier Audit PKE) is the ingestion phase expansion. Unlike previous projects, the raw documentationmust be proccessed in 2 ways. 

First ingestion pipelinemust proccess raw documentation in RAG similar fashion, meaning documents must be semanticly chunked. In detail chunking should be done by chapters and sub-chapters (for example - Chapter 1. and Chapter 1.1, but not Chapter 1.1.1.). That level of chunking will suffice to break down large documents to acceptable size that wiki framework can easiliy process. And each chunk must be stored in DB (for example sqlite), along with metadata (document name, date, chunk). 

Second ingestion pipeline start ingestion as in original wiki, independently to the 1st ingestion pipeline and similar to previous projects. But here we introduce additional proccessing step, that I call "sieving". Here is documentation that explain the sieving in details (Crumb generation). 

It is important to establish connection between sieved crumbs (2nd ingestion pipline) and chunked documents (1st ingestion pipeline).

Let me know when you're ready to continue.
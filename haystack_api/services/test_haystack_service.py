from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import EmbeddingRetriever
from haystack.schema import Document

# 初始化 DocumentStore (純記憶體)
document_store = InMemoryDocumentStore(embedding_dim=384)

retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="intfloat/e5-small-v2"
)

docs = [
    Document(content="蘋果 iPhone 15 Pro Max，搭載 A17 晶片", meta={"id": 1, "name": "iPhone 15 Pro Max", "price": 49900}),
    Document(content="三星 Galaxy S24 Ultra，搭載高效相機", meta={"id": 2, "name": "Galaxy S24 Ultra", "price": 38900}),
    Document(content="Sony WH-1000XM5 主動降噪耳機", meta={"id": 3, "name": "Sony WH-1000XM5", "price": 11900}),
    Document(content="蘋果 MacBook Pro 16 吋，配備 M3 晶片", meta={"id": 4, "name": "MacBook Pro 16", "price": 79900}),
    Document(content="Dell XPS 15 高效能筆電", meta={"id": 5, "name": "Dell XPS 15", "price": 59900}),
]

document_store.write_documents(docs)
document_store.update_embeddings(retriever=retriever)

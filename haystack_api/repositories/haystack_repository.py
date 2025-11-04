# repository/haystack_repository.py

import os
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import EmbeddingRetriever
from haystack.schema import Document

# Haystack CRUD處理器
class HaystackRepository:
    def __init__(self, index_name: str):
        self.index_name = index_name
        self.document_store = ElasticsearchDocumentStore(
            host="elasticsearch",
            # username="elastic",
            # password=os.getenv("ELASTIC_PASSWORD"),
            index=index_name,
            embedding_dim=384
        )
        self.retriever = EmbeddingRetriever(
            document_store=self.document_store,
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            model_format="sentence_transformers"
        )
    # 寫入資料 (create / update)
    def write(self, docs: list):
        self.document_store.write_documents(docs)
        self.document_store.update_embeddings(retriever=self.retriever)

        return {"status": "success", "count": len(docs), "index": self.index_name}

    # 取得所有資料
    def read(self):
        return self.document_store.get_all_documents()

    # 搜尋資料
    def search(self, query: str, top_k: int = 5):
        return self.retriever.retrieve(query=query, top_k=top_k)

    # 刪除指定資料
    def delete_by_ids(self, ids: list):
        self.document_store.delete_documents(ids=ids)

        return {"status": "deleted", "ids": ids, "index": self.index_name}

    # 刪除所有資料
    def delete_all(self):
        self.document_store.delete_documents()

        return {"status": "all_deleted", "index": self.index_name}

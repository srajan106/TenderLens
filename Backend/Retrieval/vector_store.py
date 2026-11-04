import chromadb
from Backend.Retrieval.embedding_model import EmbeddingModel


class TenderVectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="tender_documents",
            metadata={"hnsw:space": "cosine"}
        )

        self.embedding_model = EmbeddingModel()

    def add_chunks(self, chunks, tender_id):

        if not chunks:
            raise ValueError("No chunks provided")

        texts = [item["text"] for item in chunks]

        embeddings = self.embedding_model.generate_embeddings(
            texts
        )

        ids = []
        documents = []
        metadatas = []

        for index, item in enumerate(chunks):

            ids.append(
                f"{tender_id}_{item['metadata']['page']}_"
                f"{item['metadata']['chunk_id']}"
            )

            documents.append(item["text"])

            metadata = dict(item["metadata"])
            metadata["tender_id"] = tender_id

            # Chroma metadata supports scalar values
            metadatas.append(metadata)

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        return len(ids)

    def search(self, query, tender_id=None, top_k=5):

        embedding = (
            self.embedding_model.generate_query_embedding(query)
        )

        where = (
            {"tender_id": tender_id}
            if tender_id else None
        )

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            where=where
        )

        return results
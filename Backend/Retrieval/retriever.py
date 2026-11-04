from Backend.Retrieval.vector_store import TenderVectorStore


class TenderRetriever:

    def __init__(self):

        self.store = TenderVectorStore()

    def retrieve_chunks(self, question, tender_id, top_k=5):

        results = self.store.search(
            query=question,
            tender_id=tender_id,
            top_k=top_k
        )

        retrieved = []

        if not results["documents"]:
            return retrieved

        for index, document in enumerate(
            results["documents"][0]
        ):

            metadata = results["metadatas"][0][index]

            distance = results["distances"][0][index]

            retrieved.append({
                "text": document,
                "metadata": metadata,
                "distance": distance
            })

        return retrieved
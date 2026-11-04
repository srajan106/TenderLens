import json
import sys
import os

from Backend.Retrieval.vector_store import TenderVectorStore
from Backend.Retrieval.retriever import TenderRetriever


def test_retrieval():

    output_path = os.path.join(
        "Backend", "Ingestion", "ingestion_output.json"
    )

    with open(output_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    tender_id = "sample_tender"

    store = TenderVectorStore()

    count = store.add_chunks(
        data["chunks"],
        tender_id
    )

    print("Stored chunks:", count)

    retriever = TenderRetriever()

    results = retriever.retrieve_chunks(
        "What are the eligibility requirements?",
        tender_id
    )

    print("\nRetrieved results:\n")

    for result in results:

        print("Page:", result["metadata"]["page"])
        print("Text:", result["text"][:300])
        print("-" * 50)


if __name__ == "__main__":
    test_retrieval()
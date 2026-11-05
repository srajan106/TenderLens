from Backend.Generation.gemini_client import GeminiClient
from Backend.Generation.prompt_templates import create_rag_prompt


class AnswerGenerator:

    def __init__(self):

        self.gemini = GeminiClient()

    def generate_answer(self, question, retrieved_chunks):

        if not retrieved_chunks:

            return {
                "answer": (
                    "I could not find relevant information "
                    "in the selected tender document."
                ),
                "sources": []
            }

        prompt = create_rag_prompt(
            question,
            retrieved_chunks
        )

        answer = self.gemini.generate_response(prompt)

        sources = []

        for item in retrieved_chunks:

            metadata = item["metadata"]

            sources.append({
                "filename": metadata.get("filename"),
                "page": metadata.get("page"),
                "excerpt": item["text"][:300]
            })

        return {
            "answer": answer,
            "sources": sources
        }
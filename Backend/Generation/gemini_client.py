import os
from google import genai


class GeminiClient:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing from environment"
            )

        self.client = genai.Client(api_key=api_key)

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        )

    def generate_response(self, prompt):

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text or "No answer was generated."
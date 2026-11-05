from Backend.Generation.gemini_client import GeminiClient

from Backend.Generation.prompt_templates import (
    create_comparison_prompt
)


class TenderComparator:

    def __init__(self):

        self.gemini = GeminiClient()

    def compare_tenders(
        self,
        tender_a,
        tender_b,
        results_a,
        results_b
    ):

        if not results_a or not results_b:

            return {
                "comparison": (
                    "Insufficient retrieved information "
                    "to compare both tenders."
                )
            }

        prompt = create_comparison_prompt(
            tender_a,
            tender_b,
            results_a,
            results_b
        )

        comparison = self.gemini.generate_response(prompt)

        return {
            "comparison": comparison
        }
def create_rag_prompt(question, retrieved_chunks):

    context = ""

    for index, item in enumerate(retrieved_chunks, start=1):

        metadata = item["metadata"]

        context += f"""
SOURCE {index}
Document: {metadata.get('filename', 'Unknown')}
Page: {metadata.get('page', 'Unknown')}

Content:
{item['text']}

-----------------------------
"""

    prompt = f"""
You are TenderLens, an AI assistant specialized
in analyzing government tender documents.

Answer the user's question using ONLY the
provided tender document context.

Rules:
1. Do not invent facts.
2. If the answer is not available, clearly say so.
3. Use simple and professional English.
4. Include source page numbers.
5. Distinguish between explicit requirements
   and your interpretation.
6. Never assume missing tender information.

TENDER DOCUMENT CONTEXT:

{context}

USER QUESTION:
{question}

Provide:
- A clear answer.
- Relevant requirements.
- Source document and page references.
"""

    return prompt


def create_comparison_prompt(
    tender_a,
    tender_b,
    results_a,
    results_b
):

    def format_context(results):

        output = ""

        for item in results:

            metadata = item["metadata"]

            output += (
                f"Page {metadata.get('page')}: "
                f"{item['text']}\n\n"
            )

        return output

    return f"""
You are TenderLens, an AI tender comparison assistant.

Compare the following two tender documents.

TENDER A: {tender_a}

{format_context(results_a)}

TENDER B: {tender_b}

{format_context(results_b)}

Compare:
1. Eligibility criteria
2. Financial requirements
3. Experience requirements
4. Submission conditions
5. Important differences

Use a table where possible.

Only report facts supported by the provided content.
Mark missing information as "Not found in retrieved context".

Include source page numbers for each comparison.
"""
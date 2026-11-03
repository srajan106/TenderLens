
def split_into_chunks(text, chunk_size=1000, overlap=200):
    """
    Divide text into overlapping chunks.
    """

    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "Overlap must be smaller than chunk size."
        )

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):

        end = min(start + chunk_size, len(text))

        # Prefer breaking at a word boundary
        if end < len(text):
            boundary = text.rfind(" ", start, end)

            if boundary > start:
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def create_document_chunks(pages, chunk_size=1000, overlap=200):
    """
    Generate chunks while preserving page metadata.
    """

    all_chunks = []

    for page in pages:

        text = page["text"]
        metadata = page["metadata"]

        chunks = split_into_chunks(
            text,
            chunk_size,
            overlap
        )

        for index, chunk in enumerate(chunks):

            all_chunks.append({
                "text": chunk,
                "metadata": {
                    **metadata,
                    "chunk_id": index
                }
            })

    return all_chunks


import sys
import json
import os

from pdf_extractor import extract_pdf
from text_cleaner import clean_text
from chunker import create_document_chunks
from metadata_extractor import extract_metadata


def process_tender(pdf_path):

    print("\n========== TENDERLENS INGESTION ==========\n")

    # STEP 1: Extract PDF
    print("[1] Extracting PDF text...")

    pages = extract_pdf(pdf_path)

    print(f"Total pages extracted: {len(pages)}")

    # STEP 2: Clean text
    print("\n[2] Cleaning extracted text...")

    for page in pages:
        page["text"] = clean_text(page["text"])

    full_text = "\n".join(
        page["text"] for page in pages
    )

    if not full_text.strip():
        raise ValueError(
            "No text could be extracted. "
            "Check PDF quality and OCR installation."
        )

    print("Text cleaning completed.")

    # STEP 3: Extract metadata
    print("\n[3] Extracting tender metadata...")

    filename = os.path.basename(pdf_path)

    tender_metadata = extract_metadata(
        full_text,
        filename
    )

    print(json.dumps(tender_metadata, indent=4))

    # STEP 4: Generate chunks
    print("\n[4] Creating document chunks...")

    chunks = create_document_chunks(
        pages,
        chunk_size=1000,
        overlap=200
    )

    print(f"Total chunks generated: {len(chunks)}")

    if not chunks:
        raise ValueError("No document chunks were generated.")

    # STEP 5: Display sample chunk
    print("\n[5] Sample extracted chunk:\n")

    print(chunks[0]["text"][:500])

    print("\nSample metadata:")

    print(json.dumps(
        chunks[0]["metadata"],
        indent=4
    ))

    # STEP 6: Save JSON output
    output = {
        "tender_metadata": tender_metadata,
        "total_pages": len(pages),
        "total_chunks": len(chunks),
        "chunks": chunks
    }

    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "ingestion_output.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nOutput saved to: {output_path}")

    print("\n========== INGESTION COMPLETED ==========\n")

    return output


if __name__ == "__main__":

    if len(sys.argv) != 2:

        print(
            "Usage: python test_ingestion.py <tender.pdf>"
        )

        sys.exit(1)

    try:

        process_tender(sys.argv[1])

    except Exception as error:

        print(f"\nError: {error}")

        sys.exit(1)

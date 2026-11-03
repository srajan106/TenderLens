
import pymupdf
import pytesseract
from PIL import Image
import io
import os

# Tesseract OCR installation path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_pdf(pdf_path):
    """
    Extract text from digital and scanned PDF documents.
    Automatically applies OCR when a page has little or no text.
    """

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if not pdf_path.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported.")

    pages = []
    document = pymupdf.open(pdf_path)

    try:
        total_pages = len(document)

        for page_number, page in enumerate(document, start=1):

            print(f"Processing page {page_number}/{total_pages}")

            # First attempt normal text extraction
            text = page.get_text("text").strip()

            # Apply OCR if the page has very little selectable text
            if len(text) < 40:

                print(f"Page {page_number}: Applying OCR...")

                pix = page.get_pixmap(
                    matrix=pymupdf.Matrix(2, 2),
                    alpha=False
                )

                image = Image.open(
                    io.BytesIO(pix.tobytes("png"))
                )

                text = pytesseract.image_to_string(
                    image,
                    lang="eng"
                ).strip()

            pages.append({
                "text": text,
                "metadata": {
                    "filename": os.path.basename(pdf_path),
                    "page": page_number,
                    "total_pages": total_pages
                }
            })

    finally:
        document.close()

    return pages

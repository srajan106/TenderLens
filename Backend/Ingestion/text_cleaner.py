
import re


def clean_text(text):
    """
    Clean extracted PDF or OCR text.
    """

    if not text:
        return ""

    # Remove null characters
    text = text.replace("\x00", "")

    # Normalize line breaks
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces and tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove unnecessary spaces around line breaks
    text = re.sub(r" *\n *", "\n", text)

    return text.strip()

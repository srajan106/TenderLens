
import re


def extract_metadata(text, filename):

    metadata = {
        "filename": filename,
        "tender_number": None,
        "organization": None,
        "estimated_value": None,
        "submission_deadline": None
    }

    # Extract tender reference number
    tender_pattern = (
        r"(?:Tender\s*(?:No\.?|Number|ID|Reference)|"
        r"NIT\s*(?:No\.?|Number)?)\s*[:\-]?\s*"
        r"([A-Z0-9][A-Z0-9/\-]{2,})"
    )

    match = re.search(
        tender_pattern,
        text,
        re.IGNORECASE
    )

    if match:
        metadata["tender_number"] = match.group(1).strip()

    # Extract organization
    organization_pattern = (
        r"(?:Issued by|Organization|Organisation|"
        r"Department)\s*[:\-]\s*([^\n]+)"
    )

    match = re.search(
        organization_pattern,
        text,
        re.IGNORECASE
    )

    if match:
        metadata["organization"] = match.group(1).strip()

    # Extract estimated value
    value_pattern = (
        r"(?:Estimated\s+(?:Cost|Value)|"
        r"Tender\s+Value)\s*[:\-]?\s*"
        r"(?:INR|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?)"
    )

    match = re.search(
        value_pattern,
        text,
        re.IGNORECASE
    )

    if match:
        metadata["estimated_value"] = match.group(1)

    # Extract submission deadline
    deadline_pattern = (
        r"(?:Submission\s+Deadline|"
        r"Last\s+Date\s+of\s+Submission|"
        r"Bid\s+Submission\s+End\s+Date)"
        r"\s*[:\-]?\s*([^\n]+)"
    )

    match = re.search(
        deadline_pattern,
        text,
        re.IGNORECASE
    )

    if match:
        metadata["submission_deadline"] = match.group(1).strip()

    return metadata

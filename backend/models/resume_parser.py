"""
resume_parser.py — Resume File Parser
======================================
Handles parsing of uploaded resume files in PDF, DOCX, or TXT format.
Extracts raw text content for downstream NLP processing.
"""

import io
from pdfminer.high_level import extract_text as pdf_extract_text
import docx2txt


def parse_resume(file_bytes: bytes, filename: str) -> str:
    """
    Parse a resume file and return its raw text content.

    Args:
        file_bytes: Raw bytes of the uploaded file.
        filename:   Original filename (used to detect format via extension).

    Returns:
        Extracted plain-text string from the resume.

    Raises:
        ValueError: If the file extension is not supported.
    """
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if extension == "pdf":
        # pdfminer.six extracts text from PDF while preserving layout
        return pdf_extract_text(io.BytesIO(file_bytes))

    elif extension == "docx":
        # docx2txt handles .docx files including embedded images (ignored here)
        return docx2txt.process(io.BytesIO(file_bytes))

    elif extension == "txt":
        # Plain text — decode with fallback to latin-1 for non-UTF files
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return file_bytes.decode("latin-1")

    else:
        raise ValueError(
            f"Unsupported file format: .{extension}. "
            "Please upload a PDF, DOCX, or TXT file."
        )

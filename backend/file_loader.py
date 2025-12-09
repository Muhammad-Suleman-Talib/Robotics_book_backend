# backend/file_loader.py

import os
from typing import Optional
from pypdf import PdfReader
import docx


def clean_text(text: str) -> str:
    """
    Cleans the extracted text by removing excessive whitespace and common unwanted characters.
    """
    # Replace multiple newlines/spaces with a single space
    text = os.linesep.join([s for s in text.splitlines() if s]) # Remove empty lines
    text = ' '.join(text.split()) # Replace multiple spaces with single space
    # Add more cleaning rules as needed
    return text


def load_txt(file_path: str) -> Optional[str]:
    """Loads text from a .txt file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return clean_text(f.read())
    except Exception as e:
        print(f"Error loading TXT file {file_path}: {e}")
        return None


def load_pdf(file_path: str) -> Optional[str]:
    """Loads text from a .pdf file."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return clean_text(text)
    except Exception as e:
        print(f"Error loading PDF file {file_path}: {e}")
        return None


def load_md(file_path: str) -> Optional[str]:
    """Loads text from a .md or .mdx file (treating as plain text)."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return clean_text(f.read())
    except Exception as e:
        print(f"Error loading Markdown file {file_path}: {e}")
        return None


def load_docx(file_path: str) -> Optional[str]:
    """Loads text from a .docx file."""
    try:
        doc = docx.Document(file_path)
        text = [paragraph.text for paragraph in doc.paragraphs]
        return clean_text("\n".join(text))
    except Exception as e:
        print(f"Error loading DOCX file {file_path}: {e}")
        return None

def load_document(file_path: str) -> Optional[str]:
    """
    Loads and extracts text from various document types based on file extension.
    Supports .txt, .pdf, .md, .mdx, .docx.
    """
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()

    if extension == ".txt":
        return load_txt(file_path)
    elif extension == ".pdf":
        return load_pdf(file_path)
    elif extension in [".md", ".mdx"]:
        return load_md(file_path)
    elif extension == ".docx":
        return load_docx(file_path)
    else:
        print(f"Unsupported file type for {file_path}: {extension}")
        return None

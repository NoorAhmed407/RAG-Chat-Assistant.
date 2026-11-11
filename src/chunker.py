
import re


def clean_text(text):

    # Remove null characters
    text = text.replace("\x00", "")

    # Fix words split across lines by hyphenation
    text = re.sub(r"(\w+)-\s*\n\s*(\w+)", r"\1\2", text)

    # Normalize line endings
    text = text.replace("\r\n", "\n")

    # Remove excessive whitespace
    text = re.sub(r"[ \t]+", " ", text)

    # Replace multiple newlines with a single newline
    text = re.sub(r"\n{2,}", "\n", text)

    # Remove leading and trailing whitespace
    text = text.strip()

    return text


def chunk_text(text, chunk_size=500, overlap=50):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

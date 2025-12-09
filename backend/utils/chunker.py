# backend/utils/chunker.py

from typing import List


def word_chunker(text: str, chunk_size_words: int, overlap_words: int) -> List[str]:
    """
    Splits text into chunks based on word count with a specified overlap.

    Args:
        text (str): The input text to chunk.
        chunk_size_words (int): The maximum number of words per chunk.
        overlap_words (int): The number of words to overlap between consecutive chunks.

    Returns:
        List[str]: A list of text chunks.
    """
    if not text:
        return []

    words = text.split()
    chunks = []
    num_words = len(words)

    if chunk_size_words <= 0:
        raise ValueError("chunk_size_words must be a positive integer.")
    if overlap_words < 0:
        raise ValueError("overlap_words must be a non-negative integer.")
    if overlap_words >= chunk_size_words:
        raise ValueError("overlap_words must be less than chunk_size_words.")

    start_idx = 0
    while start_idx < num_words:
        end_idx = min(start_idx + chunk_size_words, num_words)
        chunk = " ".join(words[start_idx:end_idx])
        chunks.append(chunk)

        if end_idx == num_words:
            break

        start_idx += (chunk_size_words - overlap_words)
        # Ensure we don't start the next chunk before the end of the current one if overlap is too large
        if start_idx >= num_words - overlap_words and start_idx < num_words:
             # If the remaining part is too small but still needs to be included as a full chunk
             # or if the remaining part with overlap makes a valid chunk, let it be processed in the next iteration
             pass
        elif start_idx >= num_words: # If we've processed all words
            break

    return chunks

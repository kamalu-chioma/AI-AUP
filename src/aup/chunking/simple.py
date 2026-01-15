"""Simple text chunking utilities."""

from aup.errors import ChunkingError


def chunk_by_max_chars(
    text: str, max_chars: int, overlap: int = 0, preserve_words: bool = True
) -> list[str]:
    """
    Split text into chunks by maximum character count with optional overlap.

    Args:
        text: Text to chunk
        max_chars: Maximum characters per chunk
        overlap: Number of characters to overlap between chunks
        preserve_words: If True, avoid splitting words (split at word boundaries)

    Returns:
        List of text chunks

    Raises:
        ChunkingError: If max_chars is invalid
    """
    if max_chars <= 0:
        raise ChunkingError("max_chars must be greater than 0")
    if overlap < 0:
        raise ChunkingError("overlap must be non-negative")
    if overlap >= max_chars:
        raise ChunkingError("overlap must be less than max_chars")

    if len(text) <= max_chars:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chars

        if end >= len(text):
            # Last chunk
            chunks.append(text[start:])
            break

        if preserve_words:
            # Try to split at word boundary
            # Look backwards from end for whitespace
            lookback_start = max(start, end - 50)  # Look back up to 50 chars
            last_space = text.rfind(" ", lookback_start, end)
            if last_space > start:
                end = last_space + 1  # Include the space

        chunk = text[start:end]
        chunks.append(chunk)

        # Move start forward, accounting for overlap
        start = end - overlap

    return chunks


def chunk_by_tokens(
    text: str, max_tokens: int, overlap_tokens: int = 0, preserve_words: bool = True
) -> list[str]:
    """
    Split text into chunks by approximate token count.

    Uses a heuristic approximation: ~4 characters per token.
    For accurate tokenization, use a real tokenizer from your provider.

    Args:
        text: Text to chunk
        max_tokens: Maximum tokens per chunk
        overlap_tokens: Number of tokens to overlap between chunks
        preserve_words: If True, avoid splitting words

    Returns:
        List of text chunks

    Raises:
        ChunkingError: If max_tokens is invalid
    """
    if max_tokens <= 0:
        raise ChunkingError("max_tokens must be greater than 0")
    if overlap_tokens < 0:
        raise ChunkingError("overlap_tokens must be non-negative")
    if overlap_tokens >= max_tokens:
        raise ChunkingError("overlap_tokens must be less than max_tokens")

    # Approximate: 4 characters per token
    chars_per_token = 4
    max_chars = max_tokens * chars_per_token
    overlap_chars = overlap_tokens * chars_per_token

    return chunk_by_max_chars(text, max_chars, overlap_chars, preserve_words)

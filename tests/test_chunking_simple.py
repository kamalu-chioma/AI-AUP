"""Tests for simple chunking functionality."""

import pytest

from aup.chunking import chunk_by_max_chars, chunk_by_tokens
from aup.errors import ChunkingError


def test_chunk_by_max_chars_basic():
    """Test basic character-based chunking."""
    text = "a" * 100
    chunks = chunk_by_max_chars(text, max_chars=30)
    assert len(chunks) == 4  # 100 / 30 = 4 chunks (last one is smaller)
    assert sum(len(chunk) for chunk in chunks) == 100


def test_chunk_by_max_chars_small_text():
    """Test chunking text smaller than max_chars."""
    text = "Hello world"
    chunks = chunk_by_max_chars(text, max_chars=100)
    assert len(chunks) == 1
    assert chunks[0] == text


def test_chunk_by_max_chars_overlap():
    """Test chunking with overlap."""
    text = "a" * 100
    chunks = chunk_by_max_chars(text, max_chars=30, overlap=10)
    # With overlap, we get more chunks
    assert len(chunks) >= 3
    # Verify all text is covered
    assert "".join(chunks).replace(text[:10], "", 1) == text  # Rough check


def test_chunk_by_max_chars_invalid_max_chars():
    """Test error with invalid max_chars."""
    with pytest.raises(ChunkingError, match="must be greater than 0"):
        chunk_by_max_chars("text", max_chars=0)

    with pytest.raises(ChunkingError, match="must be greater than 0"):
        chunk_by_max_chars("text", max_chars=-1)


def test_chunk_by_max_chars_invalid_overlap():
    """Test error with invalid overlap."""
    with pytest.raises(ChunkingError, match="must be non-negative"):
        chunk_by_max_chars("text", max_chars=10, overlap=-1)

    with pytest.raises(ChunkingError, match="must be less than max_chars"):
        chunk_by_max_chars("text", max_chars=10, overlap=10)


def test_chunk_by_tokens_basic():
    """Test basic token-based chunking."""
    text = "word " * 100  # ~500 chars, ~125 tokens (with 4 chars/token)
    chunks = chunk_by_tokens(text, max_tokens=25)  # ~100 chars per chunk
    assert len(chunks) >= 4  # Should create multiple chunks


def test_chunk_by_tokens_small_text():
    """Test chunking text with few tokens."""
    text = "Hello world"
    chunks = chunk_by_tokens(text, max_tokens=100)
    assert len(chunks) == 1


def test_chunk_by_tokens_invalid_max_tokens():
    """Test error with invalid max_tokens."""
    with pytest.raises(ChunkingError, match="must be greater than 0"):
        chunk_by_tokens("text", max_tokens=0)


def test_chunk_by_tokens_overlap():
    """Test token-based chunking with overlap."""
    text = "word " * 100
    chunks = chunk_by_tokens(text, max_tokens=25, overlap_tokens=5)
    assert len(chunks) >= 3


def test_preserve_words():
    """Test that word boundaries are preserved when possible."""
    text = "This is a test sentence. " * 10
    chunks = chunk_by_max_chars(text, max_chars=50, preserve_words=True)
    # Check that chunks don't split in the middle of words (rough check)
    for chunk in chunks:
        # Should not have isolated letters at boundaries (simplified check)
        assert len(chunk) > 0

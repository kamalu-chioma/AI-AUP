"""
Semantic chunking utilities (stub implementation).

This module provides a placeholder for semantic/embedding-based chunking.
To implement semantic chunking:

1. Use an embedding model (e.g., from OpenAI, Cohere, or open-source models)
2. Generate embeddings for sentences or paragraphs
3. Group semantically similar chunks together
4. Use techniques like:
   - Cosine similarity thresholds
   - Recursive character splitting with semantic similarity
   - Sliding window with embedding similarity

Example approach (pseudocode):
    def chunk_semantically(text, embedding_model, similarity_threshold=0.7):
        sentences = split_into_sentences(text)
        embeddings = [embedding_model.embed(s) for s in sentences]
        chunks = []
        current_chunk = [sentences[0]]
        for i, emb in enumerate(embeddings[1:], 1):
            similarity = cosine_similarity(emb, embeddings[i-1])
            if similarity >= similarity_threshold:
                current_chunk.append(sentences[i])
            else:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentences[i]]
        chunks.append(' '.join(current_chunk))
        return chunks

AUP does not include embedding models to remain provider-agnostic and dependency-free.
Users should bring their own embedding model/client.
"""

from typing import Any

from aup.errors import AUPError


class SemanticChunkingNotImplemented(AUPError):
    """Raised when semantic chunking is attempted but not implemented."""

    pass


def chunk_semantically(text: str, **kwargs: Any) -> list[str]:
    """
    Placeholder for semantic chunking implementation.

    Args:
        text: Text to chunk
        **kwargs: Additional parameters (ignored)

    Raises:
        SemanticChunkingNotImplemented: Always, as this is a stub

    Note:
        To implement semantic chunking, bring your own embedding model
        and implement chunking logic. See module docstring for guidance.
    """
    raise SemanticChunkingNotImplemented(
        "Semantic chunking is not implemented. "
        "See aup.chunking.semantic module docstring for implementation guidance. "
        "AUP remains provider-agnostic and does not include embedding models."
    )

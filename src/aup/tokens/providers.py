"""
Provider-specific tokenizer stubs.

This module provides interfaces and stubs for real tokenizers.
AUP does not include provider SDKs to remain dependency-free and provider-agnostic.

Users should bring their own tokenizers from:
- OpenAI: tiktoken library
- Anthropic: anthropic SDK
- HuggingFace: transformers library
- Or any other tokenizer

Example usage with tiktoken (user's responsibility to install):
    import tiktoken
    encoding = tiktoken.encoding_for_model("gpt-4")
    tokens = encoding.encode(text)

Example usage with Anthropic (user's responsibility to install):
    from anthropic import Anthropic
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    tokens = client.count_tokens(text)
"""

from typing import Any, Protocol


class Tokenizer(Protocol):
    """Protocol for a tokenizer interface."""

    def encode(self, text: str) -> list[int]:
        """
        Encode text to token IDs.

        Args:
            text: Text to encode

        Returns:
            List of token IDs
        """
        ...

    def decode(self, token_ids: list[int]) -> str:
        """
        Decode token IDs to text.

        Args:
            token_ids: List of token IDs

        Returns:
            Decoded text
        """
        ...

    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text.

        Args:
            text: Text to count tokens for

        Returns:
            Token count
        """
        ...


# Placeholder function - users should implement with their tokenizer
def get_tokenizer(provider: str, model: str, **kwargs: Any) -> Tokenizer:
    """
    Get a tokenizer for a provider/model (stub implementation).

    Args:
        provider: Provider name (e.g., "openai", "anthropic")
        model: Model name
        **kwargs: Additional arguments

    Raises:
        NotImplementedError: Always, as this is a stub

    Note:
        Users should implement this with their own tokenizer.
        See module docstring for examples.
    """
    raise NotImplementedError(
        "get_tokenizer is not implemented. "
        "Bring your own tokenizer from your provider's SDK. "
        "See module docstring for examples."
    )

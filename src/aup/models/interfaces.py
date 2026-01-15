"""Protocols and interfaces for provider calls."""

from typing import Protocol


class ProviderCall(Protocol):
    """
    Protocol for a provider API call.

    This protocol defines the interface that AUP utilities expect.
    Users can wrap any provider SDK to match this interface.

    Example:
        def my_openai_call(messages: list[dict[str, str]]) -> str:
            response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
            return response.choices[0].message.content
    """

    def __call__(self, messages: list[dict[str, str]]) -> str:
        """
        Call the provider API with messages.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys

        Returns:
            Generated text response
        """
        ...

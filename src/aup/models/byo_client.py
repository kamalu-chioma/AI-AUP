"""
BYO (Bring Your Own) client patterns and examples.

This module demonstrates how to use AUP with any provider by wrapping
your provider's SDK in a callable that matches the ProviderCall protocol.

AUP does not include provider SDKs. Users bring their own clients and API keys.
"""

from typing import Callable

from aup.models.interfaces import ProviderCall

# Type alias for clarity
BYOClient = ProviderCall


def call_with_client(
    client_callable: ProviderCall,
    messages: list[dict[str, str]],
) -> str:
    """
    Call a provider client with messages (simple wrapper).

    This is a convenience function that demonstrates the pattern.
    In practice, you'd call your client directly.

    Args:
        client_callable: A callable that matches ProviderCall protocol
        messages: List of message dictionaries

    Returns:
        Generated text response

    Example:
        >>> # User's OpenAI wrapper
        >>> def openai_call(messages):
        ...     response = openai_client.chat.completions.create(
        ...         model="gpt-4",
        ...         messages=messages
        ...     )
        ...     return response.choices[0].message.content
        ...
        >>> messages = [{"role": "user", "content": "Hello"}]
        >>> result = call_with_client(openai_call, messages)
    """
    return client_callable(messages)


# Example implementations (commented out - users implement with their SDKs)
"""
# Example 1: OpenAI (user installs openai package)
import os
from openai import OpenAI

def create_openai_client(api_key: str | None = None) -> ProviderCall:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    
    def openai_call(messages: list[dict[str, str]]) -> str:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return response.choices[0].message.content
    
    return openai_call

# Example 2: Anthropic (user installs anthropic package)
from anthropic import Anthropic

def create_anthropic_client(api_key: str | None = None) -> ProviderCall:
    client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    
    def anthropic_call(messages: list[dict[str, str]]) -> str:
        # Convert to Anthropic format if needed
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=messages
        )
        return response.content[0].text
    
    return anthropic_call

# Example 3: Generic wrapper
def create_provider_client(provider_func: Callable) -> ProviderCall:
    # Wrap any provider function
    return provider_func
"""

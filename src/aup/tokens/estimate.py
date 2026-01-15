"""Token estimation utilities."""

from typing import Any

from aup.errors import TokenEstimationError

# Default pricing table (placeholder - users should update with real pricing)
# Format: {model_name: {"prompt": price_per_1k_tokens, "completion": price_per_1k_tokens}}
DEFAULT_PRICING_TABLE: dict[str, dict[str, float]] = {
    "gpt-4": {"prompt": 0.03, "completion": 0.06},
    "gpt-4-turbo": {"prompt": 0.01, "completion": 0.03},
    "gpt-3.5-turbo": {"prompt": 0.0015, "completion": 0.002},
    "claude-3-opus": {"prompt": 0.015, "completion": 0.075},
    "claude-3-sonnet": {"prompt": 0.003, "completion": 0.015},
    "claude-3-haiku": {"prompt": 0.00025, "completion": 0.00125},
    # Note: These are example prices and may be outdated
    # Users should update with current pricing from their provider
}


def estimate_tokens(text: str, chars_per_token: float = 4.0) -> int:
    """
    Estimate token count from text using a heuristic.

    Uses a simple approximation: characters / chars_per_token.
    This is a rough estimate and may not be accurate for all models or languages.

    For accurate tokenization, use a real tokenizer from your provider:
    - OpenAI: tiktoken
    - Anthropic: anthropic SDK tokenizer
    - HuggingFace: transformers tokenizers

    Args:
        text: Text to estimate tokens for
        chars_per_token: Approximate characters per token (default: 4.0)

    Returns:
        Estimated token count
    """
    if chars_per_token <= 0:
        raise TokenEstimationError("chars_per_token must be greater than 0")

    return int(len(text) / chars_per_token)


def estimate_cost(
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    pricing_table: dict[str, dict[str, float]] | None = None,
) -> float:
    """
    Estimate API cost from token counts using a pricing table.

    Args:
        model: Model name (must exist in pricing_table)
        prompt_tokens: Number of prompt tokens
        completion_tokens: Number of completion tokens
        pricing_table: Pricing table dictionary. If None, uses DEFAULT_PRICING_TABLE.

    Returns:
        Estimated cost in dollars

    Raises:
        TokenEstimationError: If model not found in pricing table

    Example:
        >>> pricing = {"gpt-4": {"prompt": 0.03, "completion": 0.06}}
        >>> cost = estimate_cost("gpt-4", 1000, 500, pricing)
        >>> print(f"${cost:.4f}")
    """
    if pricing_table is None:
        pricing_table = DEFAULT_PRICING_TABLE

    if model not in pricing_table:
        raise TokenEstimationError(
            f"Model '{model}' not found in pricing table. "
            f"Available models: {', '.join(pricing_table.keys())}"
        )

    prices = pricing_table[model]
    prompt_price_per_1k = prices.get("prompt", 0.0)
    completion_price_per_1k = prices.get("completion", 0.0)

    prompt_cost = (prompt_tokens / 1000.0) * prompt_price_per_1k
    completion_cost = (completion_tokens / 1000.0) * completion_price_per_1k

    return prompt_cost + completion_cost

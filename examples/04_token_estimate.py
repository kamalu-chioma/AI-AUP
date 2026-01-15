"""Example: Token estimation and cost calculation."""

from aup.tokens import estimate_cost, estimate_tokens


def main():
    """Demonstrate token estimation and cost calculation."""
    print("=== Token Estimation Example ===\n")

    # Example 1: Basic token estimation
    print("1. Basic token estimation:")
    texts = [
        "Hello, world!",
        "This is a longer text that we want to estimate tokens for. " * 5,
        "Short text.",
    ]

    for text in texts:
        tokens = estimate_tokens(text)
        print(f"   Text ({len(text)} chars): {tokens} estimated tokens")

    print()

    # Example 2: Custom chars_per_token
    print("2. Token estimation with custom chars_per_token:")
    text = "Hello, world! This is a sample text."
    tokens_default = estimate_tokens(text)
    tokens_custom = estimate_tokens(text, chars_per_token=3.0)
    print(f"   Text: {text}")
    print(f"   Default (4 chars/token): {tokens_default} tokens")
    print(f"   Custom (3 chars/token): {tokens_custom} tokens")
    print()

    # Example 3: Cost estimation
    print("3. Cost estimation:")
    pricing_table = {
        "gpt-4": {"prompt": 0.03, "completion": 0.06},
        "gpt-4-turbo": {"prompt": 0.01, "completion": 0.03},
        "gpt-3.5-turbo": {"prompt": 0.0015, "completion": 0.002},
        "claude-3-opus": {"prompt": 0.015, "completion": 0.075},
        "claude-3-sonnet": {"prompt": 0.003, "completion": 0.015},
    }

    scenarios = [
        ("gpt-4", 1000, 500),
        ("gpt-3.5-turbo", 2000, 1000),
        ("claude-3-opus", 1500, 750),
    ]

    for model, prompt_tokens, completion_tokens in scenarios:
        cost = estimate_cost(model, prompt_tokens, completion_tokens, pricing_table)
        print(f"   {model}: {prompt_tokens} prompt + {completion_tokens} completion tokens")
        print(f"      Cost: ${cost:.4f}")

    print()

    # Example 4: Using default pricing table
    print("4. Cost estimation with default pricing table:")
    cost = estimate_cost("gpt-4", 1000, 500)  # Uses default pricing
    print(f"   gpt-4 (1000 prompt, 500 completion): ${cost:.4f}")
    print()

    # Note about pricing
    print("Note: Pricing tables should be updated with current rates from providers.")
    print("Default pricing is provided as an example and may be outdated.")


if __name__ == "__main__":
    main()

"""Command-line interface for AUP demonstrations."""

import sys

from aup.chunking import chunk_by_max_chars, chunk_by_tokens
from aup.prompts import PromptTemplate
from aup.retries import with_retry
from aup.tokens import estimate_cost, estimate_tokens


def prompt_demo() -> None:
    """Demonstrate prompt templating."""
    print("=== Prompt Template Demo ===\n")

    template = PromptTemplate(
        system="You are a helpful {{role}}.",
        user="Explain {{topic}} in simple terms.",
        required_vars=["role", "topic"],
    )

    rendered = template.render(role="teacher", topic="Python programming")
    print("Rendered template:")
    for key, value in rendered.items():
        print(f"  {key}: {value}")

    print("\nAs messages:")
    messages = template.to_messages(rendered_vars={"role": "teacher", "topic": "Python programming"})
    for msg in messages:
        print(f"  {msg}")


def chunk_demo() -> None:
    """Demonstrate text chunking."""
    print("=== Text Chunking Demo ===\n")

    text = "This is a sample text that we want to chunk. " * 10
    print(f"Original text length: {len(text)} characters\n")

    # Character-based chunking
    chunks = chunk_by_max_chars(text, max_chars=100, overlap=20)
    print(f"Chunked by max_chars=100, overlap=20: {len(chunks)} chunks")
    for i, chunk in enumerate(chunks[:3], 1):  # Show first 3
        print(f"  Chunk {i}: {chunk[:50]}...")

    # Token-based chunking
    token_chunks = chunk_by_tokens(text, max_tokens=25, overlap_tokens=5)
    print(f"\nChunked by max_tokens=25, overlap_tokens=5: {len(token_chunks)} chunks")
    for i, chunk in enumerate(token_chunks[:3], 1):
        print(f"  Chunk {i}: {chunk[:50]}...")


def retry_demo() -> None:
    """Demonstrate retry logic."""
    print("=== Retry Logic Demo ===\n")

    attempt_count = [0]

    def flaky_function() -> str:
        attempt_count[0] += 1
        if attempt_count[0] < 3:
            raise ConnectionError(f"Attempt {attempt_count[0]} failed")
        return f"Success on attempt {attempt_count[0]}"

    print("Calling flaky function (fails twice, succeeds on third try)...")
    result = with_retry(
        flaky_function,
        retries=3,
        backoff=0.1,  # Short backoff for demo
        jitter=False,
        retry_on=(ConnectionError,),
    )
    print(f"Result: {result}")


def token_demo() -> None:
    """Demonstrate token estimation."""
    print("=== Token Estimation Demo ===\n")

    text = "This is a sample text for token estimation. " * 10
    tokens = estimate_tokens(text)
    print(f"Text: {text[:50]}...")
    print(f"Estimated tokens: {tokens}")

    # Cost estimation
    pricing = {
        "gpt-4": {"prompt": 0.03, "completion": 0.06},
        "gpt-3.5-turbo": {"prompt": 0.0015, "completion": 0.002},
    }

    print("\nCost estimation (1000 prompt tokens, 500 completion tokens):")
    for model in ["gpt-4", "gpt-3.5-turbo"]:
        cost = estimate_cost(model, 1000, 500, pricing)
        print(f"  {model}: ${cost:.4f}")


def main() -> None:
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1]

    demos = {
        "prompt-demo": prompt_demo,
        "chunk-demo": chunk_demo,
        "retry-demo": retry_demo,
        "token-demo": token_demo,
    }

    if command == "--help" or command == "-h":
        print_help()
        sys.exit(0)

    if command not in demos:
        print(f"Unknown command: {command}\n", file=sys.stderr)
        print_help()
        sys.exit(1)

    try:
        demos[command]()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def print_help() -> None:
    """Print help message."""
    print("AUP CLI - AI Utilities Pack\n")
    print("Usage: python -m aup <command>\n")
    print("Commands:")
    print("  prompt-demo    Demonstrate prompt templating")
    print("  chunk-demo     Demonstrate text chunking")
    print("  retry-demo     Demonstrate retry logic")
    print("  token-demo     Demonstrate token estimation")
    print("\nOptions:")
    print("  --help, -h     Show this help message")


if __name__ == "__main__":
    main()

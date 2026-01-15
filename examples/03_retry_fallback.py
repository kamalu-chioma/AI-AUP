"""Example: Retry and fallback utilities."""

from aup.retries import fallback_models, with_retry


def main():
    """Demonstrate retry and fallback patterns."""
    print("=== Retry and Fallback Example ===\n")

    # Example 1: Simple retry
    print("1. Retry logic with exponential backoff:")
    attempt_count = [0]

    def flaky_api_call():
        attempt_count[0] += 1
        if attempt_count[0] < 3:
            raise ConnectionError(f"API call failed (attempt {attempt_count[0]})")
        return f"Success on attempt {attempt_count[0]}"

    try:
        result = with_retry(
            flaky_api_call,
            retries=3,
            backoff=0.1,  # Short backoff for demo
            jitter=False,
            retry_on=(ConnectionError,),
        )
        print(f"   Result: {result}\n")
    except Exception as e:
        print(f"   Error: {e}\n")

    # Example 2: Retry with callback
    print("2. Retry with callback:")
    retry_log = []

    def callback(exc, attempt_num):
        retry_log.append(f"Attempt {attempt_num}: {type(exc).__name__}")

    attempt_count[0] = 0
    try:
        result = with_retry(
            flaky_api_call,
            retries=2,
            backoff=0.1,
            on_retry=callback,
        )
        print(f"   Result: {result}")
        print(f"   Retry log: {retry_log}\n")
    except Exception as e:
        print(f"   Error: {e}\n")

    # Example 3: Model fallback
    print("3. Model fallback pattern:")
    call_count = [0]

    def call_with_model(model: str) -> str:
        call_count[0] += 1
        if model == "gpt-4":
            raise ValueError("gpt-4 unavailable")
        return f"Response from {model}"

    try:
        result = fallback_models(
            ["gpt-4", "gpt-3.5-turbo", "gpt-3.5"],
            call_with_model,
            retries_per_model=1,
        )
        print(f"   Result: {result}")
        print(f"   Total calls: {call_count[0]}\n")
    except Exception as e:
        print(f"   Error: {e}\n")


if __name__ == "__main__":
    main()

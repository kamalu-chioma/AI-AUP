"""Retry logic with backoff and jitter."""

import random
import time
from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


def with_retry(
    func: Callable[[], T],
    retries: int = 3,
    backoff: float = 1.0,
    jitter: bool = True,
    retry_on: tuple[type[Exception], ...] = (Exception,),
    on_retry: Callable[[Exception, int], None] | None = None,
) -> T:
    """
    Retry a function call with exponential backoff and optional jitter.

    Args:
        func: Function to retry (should be a callable that takes no arguments)
        retries: Number of retry attempts (total attempts = retries + 1)
        backoff: Base backoff time in seconds
        jitter: If True, add random jitter to backoff time
        retry_on: Tuple of exception types to retry on
        on_retry: Optional callback called on each retry (receives exception and attempt number)

    Returns:
        Result from successful function call

    Raises:
        Last exception raised by func if all retries are exhausted

    Example:
        >>> result = with_retry(
        ...     lambda: call_api(),
        ...     retries=3,
        ...     backoff=1.0,
        ...     jitter=True,
        ...     retry_on=(ConnectionError, TimeoutError)
        ... )
    """
    last_exception = None

    for attempt in range(retries + 1):
        try:
            return func()
        except retry_on as e:
            last_exception = e

            if attempt < retries:
                # Calculate backoff time
                wait_time = backoff * (2**attempt)

                if jitter:
                    # Add random jitter (0 to 0.3 * wait_time)
                    jitter_amount = random.uniform(0, wait_time * 0.3)
                    wait_time += jitter_amount

                if on_retry:
                    on_retry(e, attempt + 1)

                time.sleep(wait_time)
            else:
                # Last attempt failed, re-raise
                raise

    # Should not reach here, but for type checking
    if last_exception:
        raise last_exception
    raise RuntimeError("Unexpected error in with_retry")


def fallback_models(
    models: list[str],
    call_func: Callable[[str], T],
    retries_per_model: int = 1,
) -> T:
    """
    Try multiple models in sequence as fallbacks.

    Attempts each model in order. If a model fails, tries the next one.
    This is a simple fallback pattern - no provider logic, just model name ordering.

    Args:
        models: List of model names to try in order
        call_func: Function that takes a model name and returns a result
        retries_per_model: Number of retries for each model before falling back

    Returns:
        Result from first successful model call

    Raises:
        Last exception if all models fail

    Example:
        >>> def call_with_model(model: str) -> str:
        ...     # Your provider call here
        ...     return client.chat.completions.create(model=model, ...)
        ...
        >>> result = fallback_models(
        ...     ["gpt-4", "gpt-3.5-turbo"],
        ...     call_with_model
        ... )
    """
    if not models:
        raise ValueError("models list cannot be empty")

    last_exception = None

    for model in models:
        try:
            return with_retry(
                lambda m=model: call_func(m),
                retries=retries_per_model,
            )
        except Exception as e:
            last_exception = e
            continue

    # All models failed
    if last_exception:
        raise last_exception
    raise RuntimeError("Unexpected error in fallback_models")

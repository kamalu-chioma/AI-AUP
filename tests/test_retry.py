"""Tests for retry functionality."""

import pytest

from aup.retries import fallback_models, with_retry


def test_retry_success_first_attempt():
    """Test retry when function succeeds immediately."""
    def success_func():
        return "success"

    result = with_retry(success_func, retries=3)
    assert result == "success"


def test_retry_success_after_failures():
    """Test retry when function succeeds after failures."""
    attempt = [0]

    def flaky_func():
        attempt[0] += 1
        if attempt[0] < 3:
            raise ValueError("Failed")
        return "success"

    result = with_retry(flaky_func, retries=3, backoff=0.01)
    assert result == "success"
    assert attempt[0] == 3


def test_retry_exhausted():
    """Test retry when all attempts fail."""
    def fail_func():
        raise ValueError("Always fails")

    with pytest.raises(ValueError, match="Always fails"):
        with_retry(fail_func, retries=2, backoff=0.01)


def test_retry_on_specific_exceptions():
    """Test retry only on specific exceptions."""
    attempt = [0]

    def func():
        attempt[0] += 1
        if attempt[0] < 2:
            raise ConnectionError("Connection failed")
        raise ValueError("Value error")

    # Should not retry on ValueError
    with pytest.raises(ValueError):
        with_retry(func, retries=3, backoff=0.01, retry_on=(ConnectionError,))


def test_on_retry_callback():
    """Test on_retry callback."""
    callbacks = []

    def flaky_func():
        if len(callbacks) < 2:
            raise ValueError("Failed")
        return "success"

    def callback(exc, attempt_num):
        callbacks.append((exc, attempt_num))

    result = with_retry(
        flaky_func,
        retries=3,
        backoff=0.01,
        on_retry=callback,
    )
    assert result == "success"
    assert len(callbacks) == 2
    assert callbacks[0][1] == 1  # First retry
    assert callbacks[1][1] == 2  # Second retry


def test_fallback_models_success_first():
    """Test fallback models when first model succeeds."""
    def call_func(model: str):
        return f"result-{model}"

    result = fallback_models(["model1", "model2"], call_func)
    assert result == "result-model1"


def test_fallback_models_success_second():
    """Test fallback models when second model succeeds."""
    attempt = [0]

    def call_func(model: str):
        attempt[0] += 1
        if model == "model1":
            raise ValueError("Model1 failed")
        return f"result-{model}"

    result = fallback_models(["model1", "model2"], call_func)
    assert result == "result-model2"


def test_fallback_models_all_fail():
    """Test fallback models when all models fail."""
    def call_func(model: str):
        raise ValueError(f"{model} failed")

    with pytest.raises(ValueError, match="model2 failed"):
        fallback_models(["model1", "model2"], call_func)


def test_fallback_models_empty_list():
    """Test fallback models with empty model list."""
    with pytest.raises(ValueError, match="cannot be empty"):
        fallback_models([], lambda m: "result")

"""Tests for token estimation functionality."""

import pytest

from aup.errors import TokenEstimationError
from aup.tokens import estimate_cost, estimate_tokens


def test_estimate_tokens_basic():
    """Test basic token estimation."""
    text = "Hello world"
    tokens = estimate_tokens(text)
    # With default 4 chars/token, "Hello world" (11 chars) = ~2-3 tokens
    assert tokens >= 2
    assert tokens <= 3


def test_estimate_tokens_custom_chars_per_token():
    """Test token estimation with custom chars_per_token."""
    text = "Hello world"  # 11 chars
    tokens = estimate_tokens(text, chars_per_token=2.0)
    # 11 / 2 = 5.5 -> 5 tokens
    assert tokens == 5


def test_estimate_tokens_invalid_chars_per_token():
    """Test error with invalid chars_per_token."""
    with pytest.raises(TokenEstimationError, match="must be greater than 0"):
        estimate_tokens("text", chars_per_token=0)

    with pytest.raises(TokenEstimationError, match="must be greater than 0"):
        estimate_tokens("text", chars_per_token=-1)


def test_estimate_cost_basic():
    """Test basic cost estimation."""
    pricing = {
        "gpt-4": {"prompt": 0.03, "completion": 0.06},
    }
    cost = estimate_cost("gpt-4", 1000, 500, pricing)
    # 1000 * 0.03 / 1000 + 500 * 0.06 / 1000 = 0.03 + 0.03 = 0.06
    assert cost == pytest.approx(0.06, rel=1e-6)


def test_estimate_cost_different_pricing():
    """Test cost estimation with different pricing."""
    pricing = {
        "gpt-3.5-turbo": {"prompt": 0.0015, "completion": 0.002},
    }
    cost = estimate_cost("gpt-3.5-turbo", 2000, 1000, pricing)
    # 2000 * 0.0015 / 1000 + 1000 * 0.002 / 1000 = 0.003 + 0.002 = 0.005
    assert cost == pytest.approx(0.005, rel=1e-6)


def test_estimate_cost_model_not_found():
    """Test error when model is not in pricing table."""
    pricing = {"gpt-4": {"prompt": 0.03, "completion": 0.06}}
    with pytest.raises(TokenEstimationError, match="not found in pricing table"):
        estimate_cost("unknown-model", 1000, 500, pricing)


def test_estimate_cost_default_pricing():
    """Test cost estimation with default pricing table."""
    # Should work with default pricing table
    cost = estimate_cost("gpt-4", 1000, 500)
    assert cost > 0


def test_estimate_cost_zero_tokens():
    """Test cost estimation with zero tokens."""
    pricing = {"gpt-4": {"prompt": 0.03, "completion": 0.06}}
    cost = estimate_cost("gpt-4", 0, 0, pricing)
    assert cost == 0.0


def test_estimate_cost_missing_completion_price():
    """Test cost estimation with missing completion price."""
    pricing = {"gpt-4": {"prompt": 0.03}}  # Missing completion
    cost = estimate_cost("gpt-4", 1000, 500, pricing)
    # Should use 0.0 for missing price
    assert cost == pytest.approx(0.03, rel=1e-6)

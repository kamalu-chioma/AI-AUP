"""Environment variable utilities."""

import os
from typing import Optional


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get an environment variable.

    Args:
        key: Environment variable name
        default: Default value if not found

    Returns:
        Environment variable value or default
    """
    return os.environ.get(key, default)


def require_env(key: str) -> str:
    """
    Require an environment variable to be set.

    Args:
        key: Environment variable name

    Returns:
        Environment variable value

    Raises:
        ValueError: If the environment variable is not set
    """
    value = os.environ.get(key)
    if value is None:
        raise ValueError(f"Required environment variable {key} is not set")
    return value

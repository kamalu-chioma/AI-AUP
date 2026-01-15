"""Type definitions and utilities."""

from typing import Any, Callable, Protocol, TypeVar

T = TypeVar("T")


class CallableWithRetries(Protocol[T]):
    """Protocol for a callable that can be retried."""

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        """Call the function."""
        ...

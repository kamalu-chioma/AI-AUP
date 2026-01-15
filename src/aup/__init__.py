"""AUP: Lightweight, provider-agnostic utilities for AI applications. Composable primitives with zero dependencies, suitable for production use."""

from aup import chunking  # noqa: F401
from aup import models  # noqa: F401
from aup import prompts  # noqa: F401
from aup import retries  # noqa: F401
from aup import tokens  # noqa: F401
from aup import utils  # noqa: F401

__all__ = [
    "chunking",
    "models",
    "prompts",
    "retries",
    "tokens",
    "utils",
]

__version__ = "0.1.0"

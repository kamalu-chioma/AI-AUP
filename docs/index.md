# AUP Documentation

Welcome to the AUP documentation!

## Overview

AUP (AI Utilities Pack) is a lightweight, provider-agnostic Python library offering small, composable primitives for AI usage.

## Documentation Structure

- [Design Principles](design.md) - Architecture, module boundaries, and design decisions
- [Philosophy](philosophy.md) - Core values and principles behind AUP

## Quick Links

- [GitHub Repository](https://github.com/yourusername/aup)
- [Contributing Guide](../CONTRIBUTING.md)
- [Examples](../examples/)

## Module Reference

### `aup.prompts`

Template and rendering utilities for building prompt messages.

**Key Classes:**
- `PromptTemplate`: System/user templates with variable substitution

**Example:**
```python
from aup.prompts import PromptTemplate

template = PromptTemplate(
    system="You are a helpful assistant.",
    user="Explain {{topic}}.",
    required_vars=["topic"]
)
messages = template.to_messages(rendered_vars={"topic": "Python"})
```

### `aup.chunking`

Text chunking utilities for processing large documents.

**Key Functions:**
- `chunk_by_max_chars()`: Character-based chunking with overlap
- `chunk_by_tokens()`: Token-based chunking (heuristic)

### `aup.tokens`

Token estimation and cost calculation.

**Key Functions:**
- `estimate_tokens()`: Approximate token count
- `estimate_cost()`: Calculate API costs

### `aup.retries`

Retry and fallback utilities.

**Key Functions:**
- `with_retry()`: Configurable retry logic
- `fallback_models()`: Model fallback helper

### `aup.models`

Provider-agnostic interfaces.

**Key Protocols:**
- `ProviderCall`: Interface for provider calls

See module docstrings for detailed API documentation.

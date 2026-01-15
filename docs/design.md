# Design Principles

This document outlines the design principles and architecture decisions for AUP.

## Core Principles

### 1. Small and Composable

Each utility in AUP is small and focused on a single responsibility. Utilities can be used independently or composed together.

**Example:**
```python
from aup.prompts import PromptTemplate
from aup.chunking import chunk_by_max_chars
from aup.retries import with_retry

# Each utility works independently
template = PromptTemplate(...)
chunks = chunk_by_max_chars(text, max_chars=1000)
result = with_retry(lambda: call_api(), retries=3)
```

### 2. Provider-Agnostic

AUP does not depend on any specific AI provider SDK. Users bring their own clients and keys.

**Pattern:**
```python
# User wraps their provider
def my_openai_call(messages):
    return openai_client.chat.completions.create(...)

# AUP utilities work with any callable
from aup.models import ProviderCall
# Use the wrapped client
```

### 3. Type Safety

Where practical, AUP uses type hints and Protocols to provide clear interfaces.

```python
from typing import Protocol

class ProviderCall(Protocol):
    def __call__(self, messages: list[dict[str, str]]) -> str: ...
```

### 4. Minimal Dependencies

AUP has zero runtime dependencies (except Python standard library). Optional dev dependencies are only for development.

## Module Boundaries

### `aup.prompts`

- **Responsibility**: Template management and message formatting
- **No dependencies**: Pure Python string manipulation
- **Input**: Templates with variables
- **Output**: Rendered strings and message lists

### `aup.chunking`

- **Responsibility**: Text segmentation
- **No dependencies**: Pure Python algorithms
- **Input**: Text, chunk size, overlap
- **Output**: List of text chunks

### `aup.tokens`

- **Responsibility**: Token estimation (heuristic)
- **No dependencies**: Mathematical approximations
- **Future**: Stub interfaces for real tokenizers
- **Input**: Text or token counts
- **Output**: Token counts or costs

### `aup.retries`

- **Responsibility**: Retry logic and fallback patterns
- **No dependencies**: Standard library only
- **Input**: Callable, retry configuration
- **Output**: Retried call results

### `aup.models`

- **Responsibility**: Interface definitions and BYO patterns
- **No dependencies**: Protocols and examples only
- **Not implementations**: Just interfaces and patterns

## Adding a New Utility

When adding a new utility to AUP:

1. **Create a new module** in `src/aup/<module_name>/`
2. **Keep it focused**: One responsibility per module
3. **No external deps**: Use standard library or add to optional deps with strong justification
4. **Add types**: Use type hints and Protocols
5. **Write tests**: Comprehensive test coverage
6. **Add examples**: Show usage in `examples/`
7. **Document**: Clear docstrings and update docs

### Example Module Structure

```
src/aup/myfeature/
  __init__.py      # Public exports
  core.py          # Main implementation
  helpers.py       # Supporting functions (if needed)
```

### Checklist

- [ ] Module has clear, single responsibility
- [ ] No vendor-specific dependencies
- [ ] Type hints on public API
- [ ] Tests in `tests/test_myfeature.py`
- [ ] Example in `examples/`
- [ ] Documentation updated
- [ ] Exported in `src/aup/__init__.py` (if appropriate)

## Error Handling

- Use custom exceptions from `aup.errors` for AUP-specific errors
- Provide clear error messages
- Fail fast with validation errors
- Let application code handle provider errors

## Performance Considerations

- Utilities are designed for reasonable performance
- No premature optimization
- Profile if performance becomes an issue
- Simple algorithms preferred over complex optimizations

## Testing Philosophy

- Test public APIs, not internals
- Fast, isolated tests
- Test edge cases and error conditions
- Use fixtures for common setups
- Mock external dependencies (rare in AUP)

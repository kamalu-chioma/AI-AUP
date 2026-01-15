# Contributing to AUP

Thank you for your interest in contributing to AUP! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/aup.git`
3. Create a virtual environment: `python -m venv .venv`
4. Install with dev dependencies: `pip install -e ".[dev]"`
5. Create a branch for your changes: `git checkout -b feature/your-feature-name`

## Development Workflow

### Code Style

- Use `ruff` for linting and formatting (configured in `pyproject.toml`)
- Run `ruff check src tests examples` before committing
- Run `ruff format src tests examples` to auto-format
- Type hints are encouraged; `mypy` is optional but recommended

### Testing

- Write tests for new features in `tests/`
- Run tests with: `pytest`
- Aim for good coverage, but focus on meaningful tests
- Tests should be fast and isolated

### Documentation

- Add docstrings to all public functions/classes (Google style)
- Update relevant docs in `docs/` if adding new modules
- Update `README.md` if adding user-facing features
- Add examples to `examples/` for new utilities

## Making Changes

### Adding a New Utility

1. Create the module in `src/aup/<module_name>/`
2. Implement the utility following existing patterns
3. Add `__init__.py` exports
4. Write tests in `tests/test_<module_name>.py`
5. Add an example in `examples/`
6. Update documentation

### Design Principles

- **Small and focused**: Each utility should do one thing well
- **Composable**: Utilities should work together or independently
- **Provider-agnostic**: No vendor-specific dependencies
- **Type-safe**: Use type hints and protocols where practical
- **Well-documented**: Clear docstrings and examples

See [docs/design.md](docs/design.md) for detailed design principles.

## Pull Request Process

1. Ensure all tests pass: `pytest`
2. Ensure code is formatted: `ruff format src tests examples`
3. Ensure linting passes: `ruff check src tests examples`
4. Update documentation as needed
5. Write a clear PR description explaining:
   - What changes were made
   - Why they were made
   - How to test them
6. Reference any related issues

## Commit Messages

Use clear, descriptive commit messages:

```
Add token estimation utility

- Implement estimate_tokens() with heuristic approximation
- Add estimate_cost() with pricing table support
- Include tests and examples
```

## Reporting Bugs

- Check existing issues first
- Create a new issue with:
  - Clear description
  - Steps to reproduce
  - Expected vs actual behavior
  - Python version and environment details

## Proposing Features

- Open an issue to discuss the feature first
- Explain the use case and design
- Consider whether it fits AUP's philosophy (see [docs/philosophy.md](docs/philosophy.md))
- Small, composable utilities are preferred over large features

## Questions?

- Open a discussion for questions
- Check existing documentation
- Review existing code for patterns

Thank you for contributing to AUP! 🎉

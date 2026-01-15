"""Custom exceptions for AUP."""


class AUPError(Exception):
    """Base exception for all AUP errors."""

    pass


class TemplateError(AUPError):
    """Error related to template rendering."""

    pass


class ValidationError(AUPError):
    """Error related to validation failures."""

    pass


class ChunkingError(AUPError):
    """Error related to text chunking."""

    pass


class TokenEstimationError(AUPError):
    """Error related to token estimation."""

    pass

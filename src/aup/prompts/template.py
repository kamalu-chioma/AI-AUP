"""Prompt template implementation."""

from typing import Any, Optional

from aup.errors import TemplateError, ValidationError


class PromptTemplate:
    """
    A template for system and user prompts with variable substitution.

    Variables are specified using {{var_name}} syntax. All required variables
    must be provided when rendering.

    Example:
        >>> template = PromptTemplate(
        ...     system="You are a {{role}}.",
        ...     user="Explain {{topic}}.",
        ...     required_vars=["role", "topic"]
        ... )
        >>> rendered = template.render(role="teacher", topic="Python")
        >>> messages = template.to_messages(rendered_vars={"role": "teacher", "topic": "Python"})
    """

    def __init__(
        self,
        system: Optional[str] = None,
        user: Optional[str] = None,
        required_vars: Optional[list[str]] = None,
        max_length: Optional[int] = None,
    ):
        """
        Initialize a prompt template.

        Args:
            system: System prompt template (optional)
            user: User prompt template (optional)
            required_vars: List of required variable names
            max_length: Maximum total length of rendered prompts (optional)

        Raises:
            ValidationError: If neither system nor user is provided
        """
        if system is None and user is None:
            raise ValidationError("At least one of 'system' or 'user' must be provided")

        self.system = system
        self.user = user
        self.required_vars = required_vars or []
        self.max_length = max_length

        # Extract variables from templates
        self._extract_variables()

    def _extract_variables(self) -> None:
        """Extract variable names from templates."""
        import re

        pattern = r"\{\{(\w+)\}\}"
        found_vars = set()

        for template in [self.system, self.user]:
            if template:
                found_vars.update(re.findall(pattern, template))

        # Validate that required_vars are present in templates
        for var in self.required_vars:
            if var not in found_vars:
                raise ValidationError(
                    f"Required variable '{var}' not found in template(s)"
                )

    def render(self, **kwargs: str) -> dict[str, str]:
        """
        Render the template with provided variables.

        Args:
            **kwargs: Variable values for substitution

        Returns:
            Dictionary with 'system' and/or 'user' keys containing rendered strings

        Raises:
            ValidationError: If required variables are missing
            TemplateError: If rendering exceeds max_length
        """
        # Check required variables
        missing_vars = set(self.required_vars) - set(kwargs.keys())
        if missing_vars:
            raise ValidationError(
                f"Missing required variables: {', '.join(sorted(missing_vars))}"
            )

        result: dict[str, str] = {}

        for key, template in [("system", self.system), ("user", self.user)]:
            if template:
                rendered = self._render_template(template, kwargs)
                result[key] = rendered

        # Check max_length
        if self.max_length:
            total_length = sum(len(v) for v in result.values())
            if total_length > self.max_length:
                raise TemplateError(
                    f"Rendered template length ({total_length}) exceeds max_length ({self.max_length})"
                )

        return result

    def _render_template(self, template: str, vars_dict: dict[str, str]) -> str:
        """
        Render a single template string.

        Args:
            template: Template string with {{var}} placeholders
            vars_dict: Dictionary of variable values

        Returns:
            Rendered string
        """
        result = template
        for var_name, var_value in vars_dict.items():
            placeholder = f"{{{{{var_name}}}}}"
            result = result.replace(placeholder, var_value)
        return result

    def to_messages(self, rendered_vars: Optional[dict[str, str]] = None) -> list[dict[str, str]]:
        """
        Convert the template to a list of message dictionaries.

        Args:
            rendered_vars: Optional variable values. If provided, template is rendered first.

        Returns:
            List of message dictionaries with 'role' and 'content' keys

        Raises:
            ValidationError: If rendering fails
        """
        if rendered_vars:
            rendered = self.render(**rendered_vars)
        else:
            # If no vars provided, return templates as-is (not recommended for production)
            rendered = {}
            if self.system:
                rendered["system"] = self.system
            if self.user:
                rendered["user"] = self.user

        messages = []
        if "system" in rendered:
            messages.append({"role": "system", "content": rendered["system"]})
        if "user" in rendered:
            messages.append({"role": "user", "content": rendered["user"]})

        return messages


# For backward compatibility and convenience
def render(template: str, **kwargs: str) -> str:
    """
    Simple template rendering function.

    Args:
        template: Template string with {{var}} placeholders
        **kwargs: Variable values

    Returns:
        Rendered string
    """
    pt = PromptTemplate(user=template)
    rendered = pt.render(**kwargs)
    return rendered.get("user", "")

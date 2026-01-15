"""Tests for prompt template functionality."""

import pytest

from aup.errors import TemplateError, ValidationError
from aup.prompts import PromptTemplate


def test_basic_template():
    """Test basic template rendering."""
    template = PromptTemplate(
        user="Hello {{name}}",
        required_vars=["name"],
    )
    rendered = template.render(name="World")
    assert rendered["user"] == "Hello World"


def test_system_and_user():
    """Test template with both system and user."""
    template = PromptTemplate(
        system="You are a {{role}}",
        user="Explain {{topic}}",
        required_vars=["role", "topic"],
    )
    rendered = template.render(role="teacher", topic="Python")
    assert rendered["system"] == "You are a teacher"
    assert rendered["user"] == "Explain Python"


def test_missing_required_var():
    """Test validation of required variables."""
    template = PromptTemplate(
        user="Hello {{name}}",
        required_vars=["name"],
    )
    with pytest.raises(ValidationError, match="Missing required variables"):
        template.render()


def test_to_messages():
    """Test conversion to message format."""
    template = PromptTemplate(
        system="You are helpful",
        user="Hello {{name}}",
        required_vars=["name"],
    )
    messages = template.to_messages(rendered_vars={"name": "World"})
    assert len(messages) == 2
    assert messages[0] == {"role": "system", "content": "You are helpful"}
    assert messages[1] == {"role": "user", "content": "Hello World"}


def test_max_length_validation():
    """Test max_length validation."""
    template = PromptTemplate(
        user="Hello {{name}}",
        required_vars=["name"],
        max_length=10,
    )
    with pytest.raises(TemplateError, match="exceeds max_length"):
        template.render(name="This is a very long name that exceeds the limit")


def test_multiple_variables():
    """Test template with multiple variables."""
    template = PromptTemplate(
        user="Hello {{greeting}}, my name is {{name}}",
        required_vars=["greeting", "name"],
    )
    rendered = template.render(greeting="Hi", name="Alice")
    assert rendered["user"] == "Hello Hi, my name is Alice"


def test_no_template_provided():
    """Test error when neither system nor user is provided."""
    with pytest.raises(ValidationError, match="At least one of"):
        PromptTemplate()


def test_required_var_not_in_template():
    """Test error when required var is not in template."""
    with pytest.raises(ValidationError, match="not found in template"):
        PromptTemplate(
            user="Hello",
            required_vars=["nonexistent"],
        )


def test_user_only_template():
    """Test template with only user prompt."""
    template = PromptTemplate(user="Hello {{name}}", required_vars=["name"])
    messages = template.to_messages(rendered_vars={"name": "World"})
    assert len(messages) == 1
    assert messages[0]["role"] == "user"


def test_system_only_template():
    """Test template with only system prompt."""
    template = PromptTemplate(system="You are helpful")
    messages = template.to_messages()
    assert len(messages) == 1
    assert messages[0]["role"] == "system"

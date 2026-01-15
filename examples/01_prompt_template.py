"""Example: Using prompt templates."""

from aup.prompts import PromptTemplate


def main():
    """Demonstrate prompt template usage."""
    print("=== Prompt Template Example ===\n")

    # Create a template
    template = PromptTemplate(
        system="You are a helpful {{role}} assistant.",
        user="Please explain {{topic}} in simple terms. Use examples if helpful.",
        required_vars=["role", "topic"],
    )

    # Render with different variables
    print("Example 1: Teacher explaining Python")
    rendered1 = template.render(role="teacher", topic="Python programming")
    print(f"System: {rendered1['system']}")
    print(f"User: {rendered1['user']}\n")

    # Convert to messages format
    print("Example 2: Converting to message format")
    messages = template.to_messages(rendered_vars={"role": "tutor", "topic": "machine learning"})
    for msg in messages:
        print(f"  {msg['role']}: {msg['content']}")
    print()

    # System-only template
    print("Example 3: System-only template")
    system_template = PromptTemplate(
        system="You are a coding assistant that writes clean, documented code.",
    )
    sys_messages = system_template.to_messages()
    print(f"Messages: {sys_messages}\n")


if __name__ == "__main__":
    main()

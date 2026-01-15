# Philosophy

This document explains the core values and principles behind AUP.

## Why AUP Exists

The AI ecosystem has many excellent frameworks, agents, and products. However, there's a gap for developers who want:

- Small, composable utilities
- No vendor lock-in
- Full control over API keys and data
- Minimal dependencies
- Simple, understandable code

AUP fills this gap by providing focused, provider-agnostic utilities that you can use however you need.

## Core Values

### 1. Neutrality

AUP is provider-agnostic. We don't prefer OpenAI over Anthropic, or any provider over another. Our utilities work with any provider as long as you can wrap it in a callable.

**Why:** Developers should choose providers based on their needs, not library constraints.

### 2. Privacy

AUP never collects telemetry, never stores API keys, and never sends data anywhere. Your data stays in your application.

**Why:** Privacy is a feature. You should trust what you use, especially when working with sensitive data.

### 3. Composability

AUP utilities are small and work independently. Use one, use many, combine them as needed.

**Why:** Real applications have diverse needs. Small, composable pieces give you flexibility.

### 4. Simplicity

AUP favors simple, readable code over clever abstractions. If a utility is hard to understand, it needs simplification.

**Why:** Simple code is maintainable, debuggable, and teachable.

### 5. Transparency

AUP's codebase is small and readable. No hidden magic, no complex abstractions that obscure behavior.

**Why:** You should understand what you're using. If you need to debug or extend, you should be able to.

## What AUP Is Not

### Not an Agent Framework

AUP doesn't orchestrate agents, manage state, or build complex workflows. It provides primitives you can use to build agents if you want.

### Not a Product

AUP isn't trying to be a commercial product. No marketing, no vendor relationships, no business model. Just utilities.

### Not Tied to Vendors

AUP doesn't depend on any provider SDK. You bring your own clients and keys. This keeps AUP lightweight and neutral.

### Not Opinionated

AUP doesn't tell you how to structure your application. Use the utilities however makes sense for your use case.

## Design Trade-offs

### Heuristics Over Accuracy

Token estimation uses simple heuristics (like chars/4) rather than real tokenizers. This keeps dependencies minimal. You can add real tokenizers if needed.

**Trade-off:** Accuracy vs. simplicity. We chose simplicity.

### Stubs Over Implementations

Some modules (like semantic chunking) are stubs with TODOs. This communicates the design space without adding dependencies.

**Trade-off:** Completeness vs. minimalism. We chose minimalism.

### BYO Client Pattern

AUP doesn't provide clients; you bring your own. This keeps AUP small and lets you use any SDK.

**Trade-off:** Convenience vs. flexibility. We chose flexibility.

## Community Values

AUP values:

- **Inclusivity**: Everyone is welcome
- **Respect**: Treat others with respect
- **Learning**: We all learn together
- **Contribution**: All contributions are valuable

See [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) for our community standards.

## Future Directions

AUP will remain:

- Small and focused
- Provider-agnostic
- Privacy-preserving
- Composable

AUP will not become:

- An agent framework
- A product with commercial features
- Tied to specific vendors
- A kitchen-sink utility library

If you need features that don't fit AUP's philosophy, that's okay! AUP is designed to work alongside other tools, not replace them.

# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the latest minor version.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not** open a public issue.

Instead, please email security concerns to the maintainers (or use GitHub's security advisory feature if available).

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if you have one)

### Response Timeline

- We aim to acknowledge receipt within 48 hours
- We will provide an initial assessment within 7 days
- We will work with you to coordinate disclosure if appropriate

## Security Philosophy

AUP is designed with security in mind:

- **No API key storage**: AUP never stores or requires API keys
- **No telemetry**: No data collection or tracking
- **Minimal dependencies**: Reduces attack surface
- **BYO keys**: You control your credentials

However, AUP is a utilities library and does not handle API key management or secure storage. It is your responsibility to:

- Store API keys securely (environment variables, secret managers, etc.)
- Use HTTPS for all API calls
- Follow your provider's security best practices
- Keep dependencies up to date

## Known Limitations

- Token estimation uses heuristics and may not be accurate
- No built-in rate limiting (implement in your application layer)
- No built-in authentication (use provider SDKs for this)

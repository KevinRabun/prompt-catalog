# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| < 1.1   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please email: **security@prompt-catalog.dev**

### What to include

- A description of the vulnerability
- Steps to reproduce the issue
- Any potential impact
- Suggested fix (if you have one)

### Response timeline

- **Acknowledgement**: Within 48 hours
- **Initial assessment**: Within 1 week
- **Fix & disclosure**: Coordinated with reporter, typically within 30 days

## Security Best Practices

When contributing to this project:

1. **Never commit secrets** — API keys, tokens, or credentials must not appear in prompts, configs, or code.
2. **Validate inputs** — The MCP server validates all prompt YAML against the JSON schema before serving.
3. **Pin dependencies** — Use exact versions or narrow ranges in `pyproject.toml`.
4. **Review prompt content** — Ensure prompt templates do not contain instructions that could lead to harmful outputs.

## Dependency Security

This project uses:
- **Dependabot** for automated dependency updates
- **GitHub vulnerability alerts** for known CVE detection
- **CI schema validation** to catch malformed prompt files

Thank you for helping keep this project secure.

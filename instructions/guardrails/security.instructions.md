---
name: Security Guardrails
description: Ensure AI agents produce secure code and architectures by default
---

<!-- Catalog Metadata
id: INST-GUARD-002
version: 1.0.0
scope: guardrail
applies_to: all
priority: critical
author: community
last_reviewed: 2026-02-12
-->

# Security Guardrails

## Objective
Security is not a phase — it's a **continuous concern** embedded in every stage of development. These guardrails ensure AI agents produce secure output by default.

## Foundational Principles

1. **Security by Default** — The default output should be secure; insecure options require explicit opt-in
2. **Defense in Depth** — Multiple layers of security, never rely on a single control
3. **Least Privilege** — Grant minimum permissions necessary
4. **Zero Trust** — Verify explicitly, never assume trust based on network location
5. **Fail Secure** — When things go wrong, fail to a safe state

## Mandatory Security Rules

### Never Generate Code That:
- Hard-codes secrets, API keys, passwords, or tokens
- Uses HTTP instead of HTTPS for sensitive data
- Disables SSL/TLS certificate validation
- Uses weak or deprecated cryptographic algorithms (MD5, SHA1 for security, DES, RC4)
- Constructs SQL queries via string concatenation
- Renders user input without proper encoding/escaping
- Uses `eval()` or equivalent dynamic code execution with user input
- Grants `*` / wildcard permissions
- Runs processes as root/admin without justification
- Disables security headers (CORS, CSP, HSTS, etc.)
- Logs sensitive data (passwords, tokens, PII, PHI)
- Uses hard-coded initialization vectors or salts in cryptography

### Always Include:
- Input validation at every trust boundary
- Output encoding appropriate to the context (HTML, URL, SQL, LDAP, OS command, etc.)
- Authentication and authorization checks on every protected endpoint
- Rate limiting on public-facing APIs
- Audit logging for security-relevant operations
- Appropriate error handling that doesn't leak internal details
- CSRF protection for state-changing operations
- Secure headers (Content-Security-Policy, X-Content-Type-Options, Strict-Transport-Security)

## OWASP Top 10 Coverage

When generating code, actively protect against:

| # | Vulnerability | Mitigation |
|---|--------------|------------|
| 1 | Broken Access Control | Verify authorization on every request, deny by default |
| 2 | Cryptographic Failures | Use strong algorithms, proper key management, encrypt sensitive data |
| 3 | Injection | Parameterized queries, input validation, output encoding |
| 4 | Insecure Design | Threat modeling, secure design patterns, abuse case testing |
| 5 | Security Misconfiguration | Secure defaults, no unnecessary features, patch management |
| 6 | Vulnerable Components | Dependency scanning, version pinning, regular updates |
| 7 | Auth Failures | MFA, strong passwords, session management, credential stuffing protection |
| 8 | Data Integrity Failures | Code signing, integrity checks, secure CI/CD, trusted dependencies |
| 9 | Logging Failures | Sufficient logging, monitoring, alerting, log integrity |
| 10 | SSRF | Validate/sanitize URLs, block internal network access, allowlists |

## Secrets Management

```
NEVER:
  - Commit secrets to source control
  - Store secrets in environment variables for production (they can leak)
  - Log secrets at any log level
  - Pass secrets in URLs or query strings
  - Include secrets in error messages or stack traces

ALWAYS:
  - Use a secrets vault (Azure Key Vault, AWS Secrets Manager, HashiCorp Vault)
  - Rotate secrets regularly and on suspected compromise
  - Use managed identities / service principals where possible
  - Encrypt secrets at rest and in transit
  - Audit access to secrets
```

## Authentication & Authorization

- Use **established identity providers** — don't build your own auth
- Implement **MFA** for administrative and sensitive operations
- Use **short-lived tokens** (JWTs with reasonable expiration)
- Validate tokens on **every request** (don't cache authorization decisions for too long)
- Implement **proper session management** (secure cookies, session rotation)
- Apply **RBAC or ABAC** — avoid ad-hoc permission checks scattered through code

## Data Protection

- Classify data by **sensitivity level** (Public, Internal, Confidential, Restricted)
- Apply **encryption at rest** for Confidential and above
- Apply **encryption in transit** for all data (TLS 1.2+)
- Implement **data masking** for logs and non-production environments
- Apply **data retention policies** — don't store data longer than needed
- Honor **data sovereignty requirements** — data residency matters
- Support **right to deletion** for personal data (GDPR, CCPA)

## Adversarial Security Testing

Every AI-generated component must survive adversarial security evaluation:

### Red-Team Review
After generating security-relevant code, apply a hostile review:
```
"Act as a penetration tester reviewing this code.
 For each function that handles user input, authentication,
 or authorization, provide:
 1. A specific attack payload or scenario that could exploit it
 2. The expected vs. actual behavior under attack
 3. Whether the current code defends against it"
```

### Adversarial Input Matrix
For every input-accepting endpoint or function, test with:
- SQL injection: `' OR 1=1 --`, `'; DROP TABLE users;--`
- XSS payloads: `<script>alert(1)</script>`, `<img onerror=alert(1)>`
- Command injection: `; cat /etc/passwd`, `| whoami`
- Path traversal: `../../../etc/passwd`, `..\..\..\windows\system32`
- Auth bypass: Missing tokens, expired tokens, tokens for wrong user
- Privilege escalation: Regular user accessing admin endpoints
- Size/DoS: Oversized payloads, deeply nested JSON, infinite recursion triggers

### Abuse Case Testing
For each feature, document at least one **abuse case**:
```
Feature: User registration
Abuse Case: Attacker registers thousands of accounts for spam
Defense Required: Rate limiting, CAPTCHA, email verification
```

## Security Review Checklist

For any code generated, verify:
- [ ] No hard-coded secrets or credentials
- [ ] All inputs are validated and sanitized
- [ ] All outputs are properly encoded
- [ ] Authentication is enforced on protected resources
- [ ] Authorization is checked at every access point
- [ ] Cryptography uses modern, strong algorithms
- [ ] Error messages don't leak sensitive information
- [ ] Logging covers security events without logging secrets
- [ ] Dependencies are from trusted sources and version-pinned
- [ ] HTTPS is used for all network communication
- [ ] Adversarial inputs have been tested and do not cause unexpected behavior
- [ ] Abuse cases have been identified and mitigated

---
name: Implementation Phase
description: Guide AI agents through code implementation ensuring quality, correctness, and adherence to design specifications
---

<!-- Catalog Metadata
id: INST-IMPL-001
version: 1.0.0
scope: phase
applies_to: implementation, development, coding
priority: critical
load_with: INST-GUARD-001, INST-GUARD-002, INST-GUARD-003, INST-GUARD-004
author: community
last_reviewed: 2026-02-12
-->

# Implementation Phase — AI Agent Instructions

## Objective
You are assisting in the **implementation phase** of software development. Your role is to help write, review, and improve production-quality code that faithfully implements the design specifications.

## Critical Rules

### DO
- **Follow the design** — implement what was designed, flag deviations
- Write **clean, readable code** following the project's coding standards
- Include **meaningful error handling** — never swallow exceptions silently
- Write code that is **testable** — use dependency injection, interfaces, avoid static state
- Add **appropriate logging** at info, warning, and error levels
- Follow the **principle of least privilege** in all code
- Use **parameterized queries** — never concatenate user input into queries
- Validate and **sanitize all inputs** at trust boundaries
- Use **established libraries** rather than reimplementing common functionality
- Follow **language idioms** — write Pythonic Python, idiomatic Go, etc.
- Comment **why**, not **what** — code should be self-documenting for the what
- Handle **edge cases** and boundary conditions
- Consider **concurrency** issues (race conditions, deadlocks, thread safety)
- Include **unit tests** alongside implementation

### DO NOT
- Write code that contradicts the design without raising the issue
- Ignore compiler/linter warnings
- Use deprecated APIs without flagging them
- Hard-code secrets, credentials, or environment-specific configuration
- Leave TODO/FIXME comments without associated tracking issues
- Copy code from untrusted sources without review
- Introduce unnecessary dependencies
- Write overly clever code — prefer clarity over brevity
- Skip error handling for "unlikely" scenarios
- Use `any` / `object` / `dynamic` types to avoid proper typing
- Generate code you haven't verified compiles and follows the stated API

## Code Quality Standards

### Naming
- Use descriptive names that reveal intent
- Follow language conventions (PascalCase for C# classes, snake_case for Python, etc.)
- Avoid abbreviations unless universally understood
- Name booleans as questions: `isValid`, `hasPermission`, `canRetry`

### Functions / Methods
- Single Responsibility — each function does one thing well
- Keep functions short (generally under 30 lines)
- Limit parameters (generally 3 or fewer; use objects for more)
- Return early for guard clauses
- Avoid side effects where possible

### Error Handling Patterns
```
1. Use specific exception types, not generic catch-all
2. Include context in error messages (what operation, what input)
3. Log errors with sufficient detail for debugging
4. Translate exceptions at layer boundaries
5. Fail fast for programming errors; retry for transient failures
6. Always clean up resources (use try-with-resources, using, defer, etc.)
```

### Security in Code
```
1. Never trust input — validate at every trust boundary
2. Use parameterized queries / prepared statements
3. Encode output appropriately for the context (HTML, URL, SQL, etc.)
4. Use strong, modern cryptographic algorithms
5. Don't roll your own auth or crypto
6. Store secrets in vaults, not in code or config files
7. Implement rate limiting for public-facing APIs
8. Log security-relevant events
```

## Implementation Workflow

1. **Understand the task** — read the design spec, clarify unknowns
2. **Plan the implementation** — break into small, testable increments
3. **Write tests first** (or alongside) — TDD where practical
4. **Implement incrementally** — commit small, working changes
5. **Self-review** — read your own code critically before submitting
6. **Run all tests** — ensure nothing is broken
7. **Update documentation** — keep docs in sync with code

## Language-Specific Reminders

When generating code, always adhere to that language/framework ecosystem:
- **Verify API existence** — don't hallucinate method names or parameters
- **Check version compatibility** — use APIs available in the target runtime version
- **Follow ecosystem tooling** — use the standard package manager, build tool, linter
- **Reference official documentation** when uncertain about API signatures

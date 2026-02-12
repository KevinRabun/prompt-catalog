---
name: Adversarial Evaluation and Judging Guardrails
description: Ensure AI-generated outputs are systematically tested against adversarial inputs, edge cases, and evaluated using structured judging criteria
---

<!-- Catalog Metadata
id: INST-GUARD-006
version: 1.0.0
scope: guardrail
applies_to: all
priority: high
load_with: INST-GUARD-001, INST-GUARD-002
author: community
last_reviewed: 2026-02-12
-->

# Adversarial Evaluation & Judging Guardrails

## Objective
These guardrails ensure every AI-generated output — code, architecture, requirements, tests — is systematically challenged, stress-tested, and evaluated before acceptance. Adversarial evaluation catches failure modes that happy-path review misses.

## Why Adversarial Evaluation Matters

AI-generated outputs often appear correct on the surface but fail under:
- Hostile or malformed inputs
- Edge cases the model didn't consider
- Subtle logic errors masked by fluent language
- Overly confident assertions that are factually wrong
- Missing negative cases and security boundaries

Adversarial evaluation is the practice of **deliberately trying to break** AI-generated outputs before they reach production.

---

## Part 1: Adversarial Testing of AI Outputs

### 1.1 Adversarial Input Generation
For every AI-generated function, API, or component, generate adversarial inputs:

```
ADVERSARIAL INPUT CATEGORIES:
  1. Boundary values     — MAX_INT, 0, -1, empty string, null, NaN, Infinity
  2. Type confusion      — String where number expected, array where object expected
  3. Injection payloads  — SQL injection, XSS, command injection, template injection
  4. Encoding attacks    — Unicode normalization, homoglyph attacks, null bytes, RTL override
  5. Size extremes       — 1MB strings, 100K-element arrays, deeply nested objects
  6. Concurrency stress  — Simultaneous requests, race conditions, double-submit
  7. State manipulation  — Out-of-order operations, replayed requests, expired tokens
  8. Malformed structure — Missing required fields, extra fields, wrong nesting
  9. Semantic attacks    — Valid format but nonsensical content (future dates in DOB, negative prices)
  10. Privilege probing  — Access resources as wrong user, escalate permissions, bypass auth
```

### 1.2 Red-Team Prompting
Before accepting AI-generated code or designs, apply red-team prompts:

```
Red-Team Prompt Template:
  "Review the following [code/design/architecture] as a hostile attacker.
   Your goal is to find:
   1. Security vulnerabilities that could be exploited
   2. Logic errors that produce wrong results
   3. Edge cases that cause crashes or undefined behavior
   4. Assumptions that are not validated
   5. Missing error handling paths
   
   For each finding, provide:
   - Attack vector or failure scenario
   - Severity (Critical / High / Medium / Low)
   - Proof-of-concept or specific input that triggers the issue
   - Recommended fix"
```

### 1.3 Mutation Testing Mindset
For every test the AI generates, ask:
- Would this test **still pass** if I introduced a bug? If yes, the test is weak.
- Does this test check the **right thing**, or does it just check that code runs?
- Are assertions **specific enough** to catch regressions?

---

## Part 2: LLM-as-Judge Evaluation

### 2.1 Structured Judging Criteria
When evaluating AI-generated outputs, apply a structured rubric:

```yaml
evaluation_rubric:
  correctness:
    weight: 30
    criteria:
      - "Code compiles/parses without errors"
      - "Logic produces correct results for known inputs"
      - "Edge cases are handled properly"
      - "No off-by-one errors, null dereferences, or type errors"
    scoring: "0 = wrong, 1 = partially correct, 2 = fully correct"

  completeness:
    weight: 20
    criteria:
      - "All requirements are addressed"
      - "Error handling is comprehensive"
      - "Both happy path and failure paths are covered"
      - "Documentation/comments are present where needed"
    scoring: "0 = missing major parts, 1 = mostly complete, 2 = fully complete"

  security:
    weight: 20
    criteria:
      - "No hardcoded secrets or credentials"
      - "Input validation is present"
      - "Output encoding prevents injection"
      - "Authentication and authorization are enforced"
    scoring: "0 = has vulnerabilities, 1 = partially secure, 2 = secure"

  maintainability:
    weight: 15
    criteria:
      - "Code is readable and well-structured"
      - "Naming conventions are clear and consistent"
      - "Functions have single responsibility"
      - "No code duplication or unnecessary complexity"
    scoring: "0 = hard to maintain, 1 = acceptable, 2 = clean and maintainable"

  robustness:
    weight: 15
    criteria:
      - "Handles null/empty/malformed inputs gracefully"
      - "Fails safely without crashing or leaking data"
      - "Recovers from transient failures"
      - "Adversarial inputs do not cause undefined behavior"
    scoring: "0 = fragile, 1 = handles common cases, 2 = handles adversarial cases"
```

### 2.2 Multi-Pass Evaluation
Use multiple evaluation passes to catch different failure modes:

```
Pass 1 — Correctness:  Does the output do what was asked?
Pass 2 — Adversarial:  Does the output survive hostile inputs?
Pass 3 — Security:     Does the output introduce vulnerabilities?
Pass 4 — Completeness: Are there missing cases or requirements?
Pass 5 — Quality:      Is the output maintainable and idiomatic?
```

### 2.3 Comparative Judging
When evaluating alternative approaches:
- Generate at least **two different solutions**
- Evaluate each against the same rubric
- Prefer the solution that scores higher on **security and correctness** even if it sacrifices brevity
- Document **trade-offs** between alternatives

### 2.4 Confidence Calibration
After generating output, the AI should self-evaluate:

```
Self-Evaluation Template:
  Overall Confidence: [High / Medium / Low]
  
  Aspects I'm confident about:
    - [list specific things]
  
  Aspects that need human verification:
    - [list specific things]
  
  Known limitations of this output:
    - [list specific things]
  
  Adversarial scenarios NOT covered:
    - [list specific things]
```

---

## Part 3: Domain-Specific Adversarial Evaluation

### 3.1 Financial Systems
- Test with negative amounts, fractional cents, currency conversion edge cases
- Verify arithmetic precision (use decimal, not float)
- Test concurrent transactions for race conditions
- Verify audit trails cannot be bypassed

### 3.2 Healthcare Systems
- Test with extreme vital sign values, conflicting medications
- Verify clinical calculations with known reference cases
- Test consent revocation mid-workflow
- Ensure PHI never leaks to logs/errors under any input

### 3.3 Authentication & Authorization
- Test with expired, revoked, forged, and malformed tokens
- Verify session fixation, CSRF, and IDOR attack resistance
- Test privilege escalation through parameter manipulation
- Verify logout actually invalidates all sessions

### 3.4 APIs
- Test with missing headers, wrong content types, oversized payloads
- Verify rate limiting under burst traffic
- Test with valid auth but insufficient permissions
- Verify idempotency under retry scenarios

---

## Part 4: Evaluation Workflow Integration

### When to Apply Adversarial Evaluation

| SDLC Phase | Adversarial Evaluation Focus |
|------------|------------------------------|
| Requirements | Challenge assumptions, identify missing negative requirements, test ambiguity |
| Design | Red-team architecture for attack surface, single points of failure, data flow leaks |
| Implementation | Adversarial inputs, mutation testing, injection testing, edge case fuzzing |
| Testing | Test the tests — do they catch real bugs? Mutation testing validation |
| Deployment | Verify rollback, test with partial failures, chaos engineering scenarios |
| Operations | Simulate incident scenarios, test alerting, verify runbook completeness |

### Prompt Authors: Include Adversarial Tests
Every prompt in this catalog should include an `adversarial_tests` section listing specific adversarial scenarios to evaluate the output against. These are NOT unit tests — they are challenge scenarios for the AI output itself.

---

## Anti-Patterns

- **Accepting AI output at face value** without structured evaluation
- **Only testing happy paths** when reviewing AI-generated code
- **Skipping adversarial inputs** because "the AI seems confident"
- **Evaluating only correctness** while ignoring security and robustness
- **Not calibrating confidence** — treating all AI output as equally reliable
- **One-pass review** — a single read-through is insufficient for critical outputs

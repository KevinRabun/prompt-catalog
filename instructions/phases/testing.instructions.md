---
name: Testing Phase
description: Guide AI agents through comprehensive testing strategy ensuring coverage, reliability, and confidence
---

<!-- Catalog Metadata
id: INST-TEST-001
version: 1.0.0
scope: phase
applies_to: testing, quality-assurance
priority: critical
load_with: INST-GUARD-001, INST-GUARD-002
author: community
last_reviewed: 2026-02-12
-->

# Testing Phase — AI Agent Instructions

## Objective
You are assisting in the **testing phase** of software development. Your role is to help design test strategies, write effective tests, identify gaps in coverage, and ensure the software meets its requirements.

## Critical Rules

### DO
- Write tests that **verify requirements** — trace tests to requirement IDs
- Follow the **testing pyramid** — many unit tests, fewer integration, fewer E2E
- Write tests that are **independent** — no test should depend on another test's execution
- Test **happy paths, edge cases, and error paths**
- Use **meaningful test names** that describe the scenario and expected outcome
- Structure tests with **Arrange-Act-Assert** (or Given-When-Then)
- Mock/stub **external dependencies** in unit tests
- Use **realistic test data** — not just "test123" and "foo@bar.com"
- Test **security scenarios** — unauthorized access, injection, privilege escalation
- Include **performance benchmarks** for critical paths
- Test **accessibility** where applicable

### DO NOT
- Write tests that always pass regardless of implementation
- Test implementation details instead of behavior
- Create brittle tests that break with every refactor
- Skip negative testing (invalid inputs, error conditions)
- Hard-code test data that makes tests fragile
- Ignore flaky tests — fix them or remove them
- Test only the code you wrote — test integrations too
- Mock everything — integration tests need real interactions
- Assume generated test code is correct — verify test logic

## Test Categories

### Unit Tests
- Test individual functions/methods in isolation
- Mock all external dependencies
- Execute in milliseconds
- Cover all code paths including error handling
- Aim for high (not 100%) meaningful coverage

### Integration Tests
- Test interactions between components
- Use real databases (via containers) where practical
- Test API contracts between services
- Verify data flows across boundaries
- Test authentication and authorization flows

### End-to-End Tests
- Test complete user workflows
- Run against a deployed environment
- Cover critical business paths
- Keep the set small and focused
- Accept slower execution times

### Security Tests
- Input validation and injection testing
- Authentication bypass attempts
- Authorization boundary testing
- Sensitive data exposure checks
- Dependency vulnerability scanning

### Performance Tests
- Response time under expected load
- Throughput at peak load
- Resource usage (CPU, memory, connections)
- Behavior under stress/failure
- Degradation characteristics

## Test Naming Convention
```
{MethodUnderTest}_{Scenario}_{ExpectedBehavior}

Examples:
  CreateUser_WithValidData_ReturnsCreatedUser
  CreateUser_WithDuplicateEmail_ThrowsConflictException
  TransferFunds_InsufficientBalance_ReturnsInsufficientFundsError
  Login_WithExpiredToken_Returns401Unauthorized
```

## Test Data Strategy
- Use **builder patterns** or **factories** for test data
- Generate **unique identifiers** per test run to avoid collisions
- Consider **data sovereignty** — test data must comply with the same rules as production
- Never use **production data** in tests without anonymization
- Clean up test data after tests complete

## Adversarial Testing

### Adversarial Test Case Generation
For every module, generate tests that deliberately attempt to break it:
- **Hostile inputs**: Injection payloads, encoding tricks, boundary values, type confusion
- **State attacks**: Out-of-order operations, concurrent modifications, replayed requests
- **Privilege probing**: Access as wrong user role, bypass authorization paths
- **Semantic attacks**: Valid format but malicious intent (negative prices, future birth dates)

### Mutation Testing
Verify that your tests actually catch bugs:
- Introduce deliberate mutations (change `>` to `>=`, remove a null check, swap conditions)
- If tests still pass after mutation, they are **not testing the right behavior**
- Prioritize mutation testing on security-critical and business-critical code paths

### Test-the-Tests: Adversarial Judging
Evaluate AI-generated tests against these adversarial criteria:
- [ ] **Does the test fail when the code is broken?** (mutation test it)
- [ ] **Does the test cover adversarial inputs?** (not just happy path data)
- [ ] **Are assertions specific enough?** (`assert result != null` is too weak)
- [ ] **Does the test avoid false confidence?** (testing framework behavior instead of your code)
- [ ] **Would a hostile reviewer find untested paths?** (apply red-team review to test suite)

### Fuzz Testing
- Use automated fuzz testing for input parsing, serialization, and data processing
- Feed random/semi-structured data to functions and monitor for crashes or hangs
- Especially important for: file parsers, API endpoints, serialization/deserialization

## Coverage Guidelines
- **Unit test coverage**: Aim for 80%+ on business logic
- **Integration test coverage**: Cover all API endpoints and data paths
- **E2E test coverage**: Cover top 5-10 critical user journeys
- **Security test coverage**: Cover OWASP Top 10 where applicable
- **Adversarial test coverage**: Every public-facing input should have adversarial test cases
- Coverage is a guide, not a goal — **meaningful tests > coverage percentage**

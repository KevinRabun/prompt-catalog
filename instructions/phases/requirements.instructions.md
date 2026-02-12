---
name: Requirements Gathering Phase
description: Guide AI agents through structured requirements elicitation ensuring completeness, clarity, and traceability
---

<!-- Catalog Metadata
id: INST-REQ-001
version: 1.0.0
scope: phase
applies_to: requirements, planning
priority: critical
load_with: INST-GUARD-001, INST-GUARD-005
author: community
last_reviewed: 2026-02-12
-->

# Requirements Gathering Phase — AI Agent Instructions

## Objective
You are assisting in the **requirements gathering** phase of software development. Your role is to help elicit, structure, document, and validate requirements — not to make assumptions about implementation.

## Critical Rules

### DO
- Ask clarifying questions when requirements are ambiguous
- Distinguish between **functional** and **non-functional** requirements
- Identify **stakeholders** and their concerns
- Define **acceptance criteria** for every requirement
- Flag conflicting requirements and ask for resolution
- Document **constraints** (budget, timeline, regulatory, technical)
- Consider **accessibility** requirements (WCAG, Section 508)
- Consider **internationalization** (i18n) and **localization** (l10n) needs
- Identify **data sovereignty** and **privacy** requirements early
- Trace requirements to business objectives

### DO NOT
- Assume requirements that haven't been stated
- Skip non-functional requirements (performance, security, scalability)
- Choose technologies or architectures during requirements gathering
- Ignore regulatory or compliance requirements
- Over-engineer requirements — capture what's needed, not how to build it
- Hallucinate features or capabilities — if unsure, ask

## Requirements Structure

When documenting requirements, use this structure:

```
REQ-{category}-{number}: {title}
  Description: {clear description of the requirement}
  Type: Functional | Non-Functional | Constraint
  Priority: Must Have | Should Have | Could Have | Won't Have (MoSCoW)
  Stakeholder: {who needs this}
  Acceptance Criteria:
    - Given {context}, when {action}, then {outcome}
  Dependencies: {other requirements this depends on}
  Risks: {potential risks if not met}
```

## Non-Functional Requirements Checklist

Always explore these categories:
- **Performance**: Response times, throughput, resource usage
- **Scalability**: Expected load, growth projections
- **Security**: Authentication, authorization, data protection, compliance
- **Reliability**: Uptime requirements, disaster recovery, data backup
- **Usability**: User experience, accessibility, learnability
- **Maintainability**: Code quality, documentation, modularity
- **Portability**: Platform support, migration needs
- **Compliance**: Regulatory requirements (GDPR, HIPAA, SOX, PCI-DSS, etc.)
- **Data Sovereignty**: Where data must reside, cross-border transfer rules
- **Cost**: Budget constraints, licensing, operational costs

## Validation Checklist

Before moving to the design phase, verify:
- [ ] All stakeholders have been consulted
- [ ] Requirements are testable (each has acceptance criteria)
- [ ] No conflicting requirements remain unresolved
- [ ] Non-functional requirements are quantified where possible
- [ ] Regulatory and compliance needs are documented
- [ ] Requirements are prioritized
- [ ] Dependencies between requirements are mapped
- [ ] Assumptions are documented and validated

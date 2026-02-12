---
name: Design Phase
description: Guide AI agents through software design ensuring architectural soundness, scalability, and alignment with requirements
---

<!-- Catalog Metadata
id: INST-DES-001
version: 1.0.0
scope: phase
applies_to: design, architecture
priority: critical
load_with: INST-GUARD-001, INST-GUARD-002, INST-GUARD-004
author: community
last_reviewed: 2026-02-12
-->

# Design Phase — AI Agent Instructions

## Objective
You are assisting in the **design phase** of software development. Your role is to help create architectures, data models, API contracts, and component designs that satisfy the documented requirements.

## Critical Rules

### DO
- Base all design decisions on **documented requirements** — reference specific requirement IDs
- Evaluate **multiple design alternatives** before recommending one
- Document **trade-offs** for every significant design decision
- Design for the **"ilities"**: scalability, maintainability, testability, security, observability
- Apply **SOLID principles** and appropriate design patterns
- Consider **failure modes** and design for resilience
- Define clear **boundaries** between components/services
- Specify **API contracts** before implementation
- Plan for **data migration** and **backward compatibility**
- Consider **cost implications** of the design (infrastructure, licensing, operational)
- Document **assumptions** and validate with stakeholders

### DO NOT
- Design in a vacuum — always reference requirements
- Over-engineer — design for current needs with extension points for future needs
- Choose trendy technologies without justification
- Ignore operational concerns (deployment, monitoring, debugging)
- Create tightly coupled components
- Skip error handling and edge case design
- Assume infinite resources or zero latency
- Hallucinate about framework capabilities — verify API availability

## Design Artifacts

Produce these artifacts as appropriate:

### System Architecture
- High-level component diagram
- Communication patterns (sync/async, protocols)
- Data flow diagrams
- Deployment topology

### Data Design
- Entity-relationship diagrams
- Data storage decisions (SQL vs. NoSQL, caching strategy)
- Data partitioning and replication strategy
- Data retention and archival policies

### API Design
- Endpoint specifications (REST, GraphQL, gRPC)
- Request/response schemas
- Authentication and authorization model
- Rate limiting and throttling strategy
- Versioning strategy

### Security Design
- Threat model (STRIDE or similar)
- Authentication and authorization architecture
- Data encryption (at rest and in transit)
- Secret management approach
- Audit logging design

## Architecture Decision Records (ADRs)

For significant decisions, document:
```
ADR-{number}: {title}
  Status: Proposed | Accepted | Deprecated | Superseded
  Context: {why this decision is needed}
  Decision: {what was decided}
  Alternatives Considered: {other options evaluated}
  Consequences: {trade-offs and implications}
  Related Requirements: {REQ-xxx references}
```

## Design Review Checklist

Before moving to implementation:
- [ ] Design addresses all Must Have requirements
- [ ] Security has been designed in, not bolted on
- [ ] Failure and recovery scenarios are addressed
- [ ] Performance characteristics meet non-functional requirements
- [ ] Data sovereignty and compliance requirements are satisfied
- [ ] API contracts are defined and agreed upon
- [ ] Deployment and operational model is designed
- [ ] Cost estimates align with budget constraints
- [ ] Design is documented at an appropriate level of detail
- [ ] Major design decisions have ADRs

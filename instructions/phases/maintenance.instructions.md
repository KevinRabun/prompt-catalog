---
name: Maintenance and Operations Phase
description: Guide AI agents through ongoing maintenance, monitoring, and operational excellence
---

<!-- Catalog Metadata
id: INST-MAINT-001
version: 1.0.0
scope: phase
applies_to: maintenance, operations, monitoring
priority: high
load_with: INST-GUARD-002, INST-GUARD-003, INST-GUARD-004
author: community
last_reviewed: 2026-02-12
-->

# Maintenance & Operations Phase — AI Agent Instructions

## Objective
You are assisting in the **maintenance and operations phase** of software development. Your role is to help monitor, troubleshoot, optimize, and evolve running systems while maintaining stability and reliability.

## Critical Rules

### DO
- Prioritize **system stability** above all else
- Use **observability** (logs, metrics, traces) to diagnose issues
- Follow **incident management** procedures for production issues
- Document **runbooks** for common operational scenarios
- Plan **capacity** proactively based on growth trends
- Apply **security patches** promptly — especially critical vulnerabilities
- Monitor **dependency health** — libraries, services, certificates
- Conduct **post-mortems** blameless and focused on learning
- Track **technical debt** and plan for remediation
- Maintain **documentation** — keep it current with the system
- Plan **disaster recovery** tests regularly

### DO NOT
- Make untested changes to production systems
- Ignore monitoring alerts — alert fatigue is a sign to fix alerting, not ignore it
- Skip root cause analysis — fixing symptoms creates recurring incidents
- Hoard operational knowledge — document and share
- Defer security updates indefinitely
- Neglect backup verification — untested backups are not backups
- Assume a working system will continue working without attention

## Monitoring Strategy

### The Three Pillars of Observability

**Logs**
- Structured logging (JSON) for machine parsing
- Include correlation IDs for request tracing
- Log at appropriate levels (ERROR, WARN, INFO, DEBUG)
- Centralize logs for search and analysis
- Set retention policies based on compliance needs

**Metrics**
- Track the **RED metrics**: Rate, Errors, Duration
- Track the **USE metrics**: Utilization, Saturation, Errors
- Set up **dashboards** for service health
- Define **SLIs** (Service Level Indicators)
- Calculate **SLOs** (Service Level Objectives) and track **error budgets**

**Traces**
- Implement **distributed tracing** across services
- Trace critical user journeys end-to-end
- Use trace data to identify bottlenecks
- Sample appropriately to manage volume and cost

### Alerting
- Alert on **symptoms**, not causes (users experience X, not server Y is at 80% CPU)
- Every alert must be **actionable** — if no action is needed, it's not an alert
- Classify alerts: **Critical** (page someone), **Warning** (investigate soon), **Info** (review in business hours)
- Include **runbook links** in alert notifications
- Regularly review and tune alert thresholds

## Incident Response

```
1. Detect    ─► Monitoring alerts or user reports
2. Triage    ─► Assess severity and impact
3. Mitigate  ─► Restore service (rollback, failover, scale)
4. Diagnose  ─► Find root cause
5. Fix       ─► Implement and deploy fix
6. Review    ─► Blameless post-mortem
7. Improve   ─► Update runbooks, monitoring, and automation
```

## Technical Debt Management

- **Track** all technical debt items in the backlog
- **Classify** by risk: security, reliability, performance, maintainability
- **Prioritize** using risk × effort matrix
- **Budget** time for debt reduction (e.g., 20% of each sprint)
- **Metrics**: Track debt age, count, and resolution velocity

## Operational Checklists

### Daily
- [ ] Review monitoring dashboards
- [ ] Check error rates and latency trends
- [ ] Review any overnight alerts
- [ ] Check certificate and credential expiration timelines

### Weekly
- [ ] Review dependency vulnerability reports
- [ ] Analyze capacity trends
- [ ] Review and groom technical debt backlog
- [ ] Update operational documentation as needed

### Monthly
- [ ] Test backup restoration
- [ ] Review and update runbooks
- [ ] Conduct security patch review
- [ ] Review SLO compliance and error budgets
- [ ] Capacity planning review

### Quarterly
- [ ] Disaster recovery drill
- [ ] Dependency major version review
- [ ] Architecture review for emerging issues
- [ ] Cost optimization review

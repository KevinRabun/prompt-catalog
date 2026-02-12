---
name: Deployment Phase
description: Guide AI agents through safe, repeatable, and auditable deployment practices
---

<!-- Catalog Metadata
id: INST-DEPLOY-001
version: 1.0.0
scope: phase
applies_to: deployment, release, ci-cd
priority: critical
load_with: INST-GUARD-002, INST-GUARD-003
author: community
last_reviewed: 2026-02-12
-->

# Deployment Phase — AI Agent Instructions

## Objective
You are assisting in the **deployment phase** of software development. Your role is to help create reliable, repeatable, and safe deployment processes that minimize risk and maximize confidence.

## Critical Rules

### DO
- Treat **infrastructure as code** (IaC) — no manual configuration in production
- Ensure deployments are **repeatable and idempotent**
- Implement **automated rollback** capabilities
- Use **feature flags** for risky changes
- Deploy to **staging** before production — always
- Run **smoke tests** after deployment
- Implement **health checks** and readiness probes
- Use **blue-green** or **canary** deployment strategies for production
- Encrypt **secrets** — use vault services, never commit secrets to source control
- Tag and version **all artifacts** (containers, packages, builds)
- Log all deployment activities for **audit trails**
- Consider **data sovereignty** in deployment topology — data residency matters
- Plan for **zero-downtime deployments** where required

### DO NOT
- Deploy directly to production without a staging environment
- Store secrets in source control, environment files, or container images
- Deploy without automated tests passing
- Make manual changes to production environments
- Skip database migration testing
- Deploy on Fridays (or before holidays / low-staffing periods) without explicit approval
- Ignore deployment monitoring after release
- Use `latest` tags for container images in production
- Grant overly broad permissions to deployment pipelines

## Deployment Pipeline Stages

```
1. Source ─► 2. Build ─► 3. Test ─► 4. Security Scan ─► 5. Stage ─► 6. Approve ─► 7. Production
     │            │           │              │                │           │              │
   Lint       Compile      Unit          SAST/DAST       Integration  Manual/Auto   Canary/BG
   Format     Package      Integration   Dependency       Smoke       Gate           Monitor
   Validate   Sign         Contract      Container        Performance                Rollback
```

## Infrastructure as Code

### Principles
- All infrastructure defined in version-controlled code
- Changes go through the same PR/review process as application code
- Use **modules** for reusable infrastructure patterns
- Parameterize environment-specific values
- Use **state management** (Terraform state, Pulumi state) securely
- Plan before apply — always review what will change

### Environment Parity
- Development, staging, and production should use the **same IaC templates**
- Differences should be limited to **size/scale parameters**
- Use the same **networking patterns** across environments
- Test IaC changes in lower environments first

## Database Migrations

- Migrations must be **forward-compatible** — old code should work with new schema
- Never delete columns/tables in the same release that removes the code using them
- Use **migration frameworks** (Flyway, Liquibase, EF Migrations, Alembic)
- Test migrations against a copy of production data volume
- Plan for **rollback** of migrations (backward-compatible changes only)
- Monitor migration performance — large table changes can lock production

## Security in Deployment

- Scan containers for vulnerabilities before deployment
- Sign artifacts and verify signatures before deployment
- Use **least-privilege** service accounts for deployment pipelines
- Rotate credentials after deployment if compromise is possible
- Enable **audit logging** for all deployment actions
- Restrict who can approve and execute production deployments

## Post-Deployment Checklist

- [ ] Smoke tests pass in production
- [ ] Health check endpoints responding
- [ ] Error rates are within acceptable thresholds
- [ ] Response times are within SLA
- [ ] Monitoring and alerting are active
- [ ] Rollback plan has been tested
- [ ] Deployment is documented in the change log
- [ ] Relevant stakeholders have been notified

# Changelog

All notable changes to the Prompt Catalog will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-13

### Added
- **MCP Server Package** (`server/`) — Working Python MCP server exposing all prompts and instructions as MCP resources and prompt templates
- **CLI Tool** (`prompt-catalog` command) — Local CLI with list, search, show, kit management, interactive guided mode, and MCP server launcher
- **Starter Kits** (`starter-kits/`) — 6 opinionated prompt+instruction bundles:
  - `saas-web-app` — Full-stack SaaS (Next.js, Rails, Django)
  - `api-backend` — REST/GraphQL API services
  - `mobile-app` — iOS, Android, cross-platform
  - `cloud-native` — Microservices, Kubernetes, serverless
  - `fintech-platform` — Financial services with compliance
  - `healthcare-app` — HIPAA-compliant clinical applications
- **Case Studies** (`case-studies/`) — Real-world analysis of 4 open-source projects:
  - Sentry (getsentry/sentry) — Cloud-native SaaS, multi-tenancy, observability
  - Medplum (medplum/medplum) — Healthcare, HIPAA, HL7 FHIR
  - Maybe Finance (maybe-finance/maybe) — FinTech, decimal arithmetic, reconciliation
  - Cal.com (calcom/cal.com) — SaaS scheduling, timezone handling, OAuth
- **Tutorial** (`tutorials/`) — "Build a SaaS Task Manager from Zero" end-to-end walkthrough using the `saas-web-app` starter kit, covering 8 prompts with filled-in variables, representative AI output, and analysis of what each prompt catches
- Catalog loader engine with filtering by category, platform, skill level, tag, and free-text search
- Interactive `prompt-catalog start` command that recommends prompt stacks based on project type

### Changed
- Updated README with CLI quickstart, starter kit table, and case study links
- Updated index.json with starter kit and case study references
- Repository structure expanded with `server/`, `starter-kits/`, and `case-studies/` directories

## [1.0.0] - 2026-02-12

### Added
- Initial prompt catalog structure
- JSON schemas for prompt and instruction validation
- Planning prompts: requirements gathering, user stories, project scoping
- Architecture prompts: system design, microservices, cloud architecture, data modeling
- Development prompts: web, Windows, Linux, Android, iOS, cross-platform, API
- Testing prompts: unit testing, integration testing, security testing, performance
- Security prompts: threat modeling, code review, compliance checking
- Deployment prompts: CI/CD, IaC, containerization, release management
- Operations prompts: monitoring, incident response, SRE practices
- Domain-specific prompts: FinTech, real estate, blockchain, game dev, compliance, data sovereignty
- SDLC phase instruction files (requirements through maintenance)
- Guardrail instruction files (accuracy, security, cost, performance, anti-hallucination)
- Platform instruction files (web, Windows, Linux, Android, iOS, cloud)
- MCP server integration configuration
- Master index for programmatic access
- Contributing guidelines and code of conduct

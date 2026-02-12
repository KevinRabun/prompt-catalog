# Prompt Catalog

[![CI](https://github.com/KevinRabun/prompt-catalog/actions/workflows/ci.yml/badge.svg)](https://github.com/KevinRabun/prompt-catalog/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Prompts](https://img.shields.io/badge/prompts-35-blue)](#coverage)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)

An open-source, community-driven library of prompts and instruction files for AI-assisted software development. Designed to be **human-readable** for review and **machine-readable** for ingestion by MCP servers, AI agents, and automation tooling.

## Vision

Building software with AI should be **accurate, secure, cost-effective, performant, and trustworthy**. This catalog provides structured prompts and guardrail instructions that help AI agents stay on track across every phase of the software development lifecycle — from requirements gathering through production operations.

## Who Is This For?

| Audience | How They Use It |
|----------|----------------|
| **Non-technical SMEs** | Use planning and requirements prompts to communicate ideas clearly to AI agents |
| **Junior Developers** | Follow guided prompts for implementation, testing, and learning best practices |
| **Senior Developers** | Leverage architecture, optimization, and domain-specific prompts |
| **Architects** | Use system design, cloud architecture, and compliance prompts |
| **DevOps / SRE** | Use deployment, monitoring, and operations prompts |
| **AI Agent Authors** | Ingest prompts and instructions via MCP server integration |

## Coverage

### Platforms & Targets
- **Web** — Frontend (React, Angular, Vue, Svelte, etc.), Backend (Node.js, .NET, Java, Python, Go, Rust)
- **Windows** — WinUI 3, WPF, MAUI, Win32, UWP
- **Linux** — CLI tools, daemons, desktop (GTK, Qt), embedded
- **Android** — Kotlin, Java, Jetpack Compose, Flutter, React Native
- **iOS** — Swift, SwiftUI, UIKit, Flutter, React Native
- **Cross-Platform** — .NET MAUI, Flutter, React Native, Electron, Tauri

### Architecture Patterns
- N-tier / Layered
- Microservices
- Event-driven / CQRS
- Serverless
- Modular monolith
- Hexagonal / Clean architecture

### Cloud Providers
- Microsoft Azure
- Amazon Web Services (AWS)
- Google Cloud Platform (GCP)
- Oracle Cloud Infrastructure (OCI)
- Multi-cloud and hybrid

### Industry Domains
- FinTech & Financial Services
- Real Estate & PropTech
- Blockchain & Web3
- Game Development
- Healthcare & Life Sciences
- Regulatory Compliance & GRC
- Data Sovereignty & Privacy
- E-commerce & Retail
- Simulation & Training Systems
- Live Virtual Constructive (LVC) Integration
- Contract Lifecycle Management (CLM)
- Legal Technology (LegalTech)
- Marketing Technology (MarTech)
- Human Resources (HRIS)
- Recruiting & Talent Acquisition
- Education & EdTech

## Repository Structure

```
prompt-catalog/
├── README.md                       # This file
├── LICENSE                         # MIT License
├── CONTRIBUTING.md                 # How to contribute
├── CODE_OF_CONDUCT.md              # Community standards
├── CHANGELOG.md                    # Version history
│
├── schema/                         # JSON Schemas for validation
│   ├── prompt.schema.json          # Schema for prompt files
│   └── instruction.schema.json     # Schema for instruction files
│
├── prompts/                        # Prompt library (YAML format)
│   ├── index.json                  # Master index for MCP ingestion
│   ├── planning/                   # Requirements & project planning
│   ├── architecture/               # System design & architecture
│   ├── development/                # Implementation prompts by platform
│   ├── testing/                    # Testing strategies & prompts
│   ├── security/                   # Security review & hardening
│   ├── deployment/                 # CI/CD, IaC, release management
│   ├── operations/                 # Monitoring, incident response
│   └── domains/                    # Industry-specific prompts
│
├── instructions/                   # Instruction files for AI agents
│   ├── phases/                     # SDLC phase guardrails
│   ├── guardrails/                 # Cross-cutting concerns
│   └── platforms/                  # Platform-specific guidance
│
├── server/                         # MCP server + CLI (Python package)
│   ├── pyproject.toml              # Package configuration
│   ├── README.md                   # Installation & usage docs
│   └── prompt_catalog_mcp/         # Python package
│       ├── catalog.py              # Catalog loader & filter engine
│       ├── server.py               # MCP server implementation
│       └── cli.py                  # CLI tool (prompt-catalog command)
│
├── starter-kits/                   # Opinionated prompt+instruction bundles
│   ├── saas-web-app.yaml           # Full-stack SaaS
│   ├── api-backend.yaml            # API service
│   ├── mobile-app.yaml             # Mobile application
│   ├── cloud-native.yaml           # Microservices / cloud-native
│   ├── fintech-platform.yaml       # FinTech with compliance
│   └── healthcare-app.yaml         # HIPAA-compliant healthcare
│
├── case-studies/                   # Real-world project analyses
│   ├── sentry-error-tracking.md    # Sentry — cloud-native SaaS
│   ├── medplum-healthcare.md       # Medplum — healthcare/FHIR
│   ├── maybe-personal-finance.md   # Maybe — personal finance
│   └── calcom-scheduling-saas.md   # Cal.com — scheduling SaaS
│
├── tutorials/                      # Step-by-step guided tutorials
│   └── build-saas-from-zero.md     # Build a SaaS app from scratch
│
└── mcp/                            # MCP integration guide
    ├── README.md                   # Integration guide
    └── server-config.json          # MCP server configuration
```

## Prompt Format

All prompts use **YAML** for human readability with a consistent schema that supports machine parsing. Each prompt includes:

```yaml
id: "PLAN-REQ-001"
version: "1.0.0"
title: "Gather Functional Requirements"
description: "Guides an AI agent through structured requirements elicitation"
category: "planning"
subcategory: "requirements"
skill_level: "beginner"           # beginner | intermediate | advanced | expert
platforms: ["all"]
tags: ["requirements", "planning", "stakeholder"]
author: "community"
last_reviewed: "2026-02-12"

prompt: |
  The actual prompt text goes here...

variables:
  - name: "project_type"
    description: "Type of software project"
    required: true
    examples: ["web-app", "mobile-app", "api-service"]

expected_output: "Structured requirements document"
quality_criteria:
  - "All functional areas covered"
  - "Acceptance criteria defined for each requirement"
```

## Instruction Files

Instruction files are Markdown documents designed to be loaded as system-level context for AI agents. They provide guardrails across:

- **SDLC Phases** — Keep agents focused on the current development phase
- **Guardrails** — Enforce accuracy, security, cost, performance, and anti-hallucination practices
- **Platforms** — Platform-specific conventions, APIs, and pitfalls

## MCP Server Integration

The catalog ships with a working [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server. Install it once and every MCP-compatible AI client (Claude Desktop, VS Code, Cursor, etc.) can access all prompts and instructions as first-class resources.

```bash
# Install from PyPI
pip install prompt-catalog

# Or install from source (for contributors)
cd server && pip install -e .

# Start the server
prompt-catalog serve
```

See [server/README.md](server/README.md) for Claude Desktop and VS Code configuration.

## Getting Started

### Quick Start with the CLI

The fastest way to get started is the interactive CLI:

```bash
# Install from PyPI
pip install prompt-catalog

# Or install from source
cd server && pip install -e .

# Interactive guided mode — recommends prompts based on your project
prompt-catalog start

# List all prompts
prompt-catalog list

# Search by keyword
prompt-catalog search "authentication"

# View a specific prompt
prompt-catalog show SEC-THREAT-001

# List starter kits
prompt-catalog kit list

# Export a kit's prompts and instructions to your project
prompt-catalog kit export saas-web-app --output ./my-project/.prompts
```

### Use a Starter Kit

Don't know where to start? Pick a [starter kit](starter-kits/):

| Kit | Best For |
|-----|----------|
| `saas-web-app` | Next.js, Rails, Django SaaS products |
| `api-backend` | REST/GraphQL API services |
| `mobile-app` | iOS, Android, Flutter, React Native |
| `cloud-native` | Kubernetes, microservices, serverless |
| `fintech-platform` | Banking, payments, trading (with compliance) |
| `healthcare-app` | HIPAA, HL7 FHIR, clinical applications |

### MCP Server Integration

Serve the entire catalog as an MCP server for Claude Desktop, VS Code, or any MCP-compatible client:

```bash
prompt-catalog serve
```

See [server/README.md](server/README.md) for configuration details.

### Follow the Tutorial

New to the catalog? Start here:

> **[Build a SaaS Task Manager from Zero](tutorials/build-saas-from-zero.md)** — A complete walkthrough of building a team task management app using the `saas-web-app` starter kit. Shows every prompt, every variable fill-in, and what the prompts catch that you'd otherwise miss.

### Browse Prompts
Navigate the `prompts/` directory organized by SDLC phase, or use the master `prompts/index.json` to search programmatically.

### Use Manually
1. Find a relevant prompt in `prompts/`
2. Fill in the `variables` with your project specifics
3. Paste into your AI assistant of choice

### Learn from Case Studies

See how the catalog applies to real open-source projects in [case-studies/](case-studies/):
- **Sentry** — Error tracking platform (microservices, multi-tenancy, observability)
- **Medplum** — Healthcare infrastructure (HIPAA, FHIR, PHI)
- **Maybe** — Personal finance app (decimal arithmetic, reconciliation)
- **Cal.com** — Scheduling SaaS (timezone handling, OAuth, race conditions)

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Adding new prompts
- Improving existing prompts
- Adding domain coverage
- Reviewing and testing prompts
- Translating prompts

## Principles

1. **Accuracy over speed** — Prompts should guide AI to verify before asserting
2. **Security by default** — Security is not optional; it's embedded in every phase
3. **Cost-awareness** — Both in AI token usage and in the software being built
4. **Performance-conscious** — Prompts should guide toward performant solutions
5. **Anti-hallucination** — Explicit instructions to cite sources, admit uncertainty, and verify
6. **Adversarial evaluation** — Every output is stress-tested with hostile inputs, judged against rubrics, and red-teamed
7. **Trust through transparency** — Every prompt is reviewable, versioned, and testable
8. **Progressive complexity** — Support users from beginner to expert
9. **Platform-agnostic where possible** — Abstract patterns, specific implementations

## License

This project is licensed under the [MIT License](LICENSE).

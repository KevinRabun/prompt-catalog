# Prompt Catalog

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
└── mcp/                            # MCP server integration
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

The catalog is designed for ingestion by [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers. The `mcp/` directory contains configuration and documentation for:

- Serving prompts as MCP resources
- Providing instruction files as context
- Filtering prompts by category, platform, skill level, or domain
- Version-aware prompt retrieval

## Getting Started

### Browse Prompts
Navigate the `prompts/` directory organized by SDLC phase, or use the master `prompts/index.json` to search programmatically.

### Use with an AI Agent
1. Clone this repository:
   ```bash
   git clone https://github.com/KevinRabun/prompt-catalog.git
   ```
2. Point your MCP server at the `mcp/server-config.json`
3. Prompts and instructions become available as context

### Use Manually
1. Find a relevant prompt in `prompts/`
2. Fill in the `variables` with your project specifics
3. Paste into your AI assistant of choice

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

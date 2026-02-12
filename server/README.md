# Prompt Catalog MCP Server & CLI

A working MCP server and command-line tool for the [Prompt Catalog](https://github.com/KevinRabun/prompt-catalog).

## Installation

```bash
# Install from PyPI (recommended)
pip install prompt-catalog

# Or install from source
cd server
pip install -e .

# Or install directly from GitHub
pip install git+https://github.com/KevinRabun/prompt-catalog.git#subdirectory=server
```

**Requirements:** Python 3.11+

## CLI Usage

```bash
# List all prompts
prompt-catalog list

# Filter by category
prompt-catalog list --category domains
prompt-catalog list --platform web --skill intermediate

# Search prompts
prompt-catalog search fintech
prompt-catalog search "threat model"

# Show full prompt details
prompt-catalog show DOM-FINTECH-001
prompt-catalog show sec-threat-001 --raw    # Raw YAML

# Starter kits
prompt-catalog kit list
prompt-catalog kit show saas-web-app
prompt-catalog kit export saas-web-app --output ./my-project

# Interactive guided mode
prompt-catalog start

# Start MCP server
prompt-catalog serve
```

## Interactive Mode

Run `prompt-catalog start` for a guided experience:

```
$ prompt-catalog start

┌─────────────────────────────────────────────┐
│ Welcome to Prompt Catalog                   │
│                                             │
│ Answer a few questions and I'll recommend   │
│ the right prompts, instructions, and        │
│ starter kit for your project.               │
└─────────────────────────────────────────────┘

What are you building?
  1. Web application (SaaS, portal, dashboard)
  2. Mobile app (Android, iOS, or cross-platform)
  3. API / Backend service
  ...

> 1

Target platform(s)?
> Web

Your experience level?
> intermediate

────────────────────────────────────────────────
Recommended Prompt Stack

Prompts:
  ✓ 1. PLAN-REQ-001 — Functional Requirements Elicitation [beginner]
  ✓ 2. PLAN-REQ-003 — User Story and Acceptance Criteria [intermediate]
  ✓ 3. ARCH-SYS-001 — System Architecture Design [intermediate]
  ✓ 4. DEV-WEB-001 — Web Application Development [intermediate]
  ...

Instructions to load:
  ✓ accuracy.instructions — Always — anti-hallucination guardrails
  ✓ security.instructions — Always — security baseline
  ✓ web.instructions — Platform — web guidance

Matching starter kit:
  → saas-web-app — SaaS Web Application
```

## MCP Server

### With Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "prompt-catalog": {
      "command": "prompt-catalog",
      "args": ["serve"],
      "env": {
        "CATALOG_ROOT": "/path/to/prompt-catalog"
      }
    }
  }
}
```

### With VS Code / Copilot

Add to your MCP settings:

```json
{
  "mcpServers": {
    "prompt-catalog": {
      "command": "prompt-catalog",
      "args": ["serve"],
      "env": {
        "CATALOG_ROOT": "c:\\Source\\prompt-catalog"
      }
    }
  }
}
```

### Capabilities

The MCP server exposes:

| Capability | Description |
|-----------|-------------|
| **Resources** | All 32 prompts + 18 instruction files as readable resources |
| **Prompt Templates** | All prompts with `{{variable}}` substitution |
| **Filtering** | Category, skill level, platform, and tag-based filtering |

## Development

```bash
git clone https://github.com/KevinRabun/prompt-catalog.git
cd prompt-catalog/server
pip install -e ".[dev]"
```

# MCP Server Integration Guide

This directory contains configuration and documentation for integrating the Prompt Catalog with [Model Context Protocol (MCP)](https://modelcontextprotocol.io) servers.

## Overview

The Prompt Catalog is designed to be consumed by MCP servers as **resources** and **prompts**, making the entire library available to AI agents and coding assistants through a standardized protocol.

## Integration Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│  AI Agent /      │────▶│  MCP Server  │────▶│  Prompt Catalog │
│  IDE Extension   │◀────│  (Resource   │◀────│  (YAML files +  │
│  (Claude, etc.)  │     │   Provider)  │     │   Instructions) │
└─────────────────┘     └──────────────┘     └─────────────────┘
```

## How It Works

### 1. Resource-Based Access

Each prompt YAML file and instruction Markdown file is exposed as an MCP **resource**:

- **URI Pattern**: `prompt-catalog://prompts/{category}/{id}` or `prompt-catalog://instructions/{scope}/{filename}`
- **MIME Type**: `text/yaml` for prompts, `text/markdown` for instructions
- **Metadata**: Category, skill level, platforms, tags from the YAML frontmatter

### 2. Prompt Templates

Prompts with `{{variables}}` are exposed as MCP **prompt templates**, allowing agents to fill in variables dynamically:

```json
{
  "name": "plan-req-001",
  "description": "Functional Requirements Elicitation",
  "arguments": [
    { "name": "project_description", "required": true },
    { "name": "stakeholders", "required": true },
    { "name": "project_constraints", "required": false }
  ]
}
```

### 3. Discovery and Filtering

The master index (`prompts/index.json`) enables programmatic discovery:

- Filter by category, subcategory, skill level, platform, or tags
- Chain prompts using `chain_position` metadata
- Load instruction files based on `load_with` recommendations

## Server Configuration

See `server-config.json` for the reference MCP server configuration.

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `catalogRoot` | Path to the prompt-catalog repository | `.` |
| `indexPath` | Path to the master index file | `prompts/index.json` |
| `enableInstructions` | Whether to serve instruction files as resources | `true` |
| `enablePromptTemplates` | Whether to expose prompts as MCP prompt templates | `true` |
| `defaultSkillLevel` | Filter prompts to this skill level and below | `"expert"` |
| `platformFilter` | Only serve prompts for these platforms | `[]` (all) |

## Building an MCP Server

### Minimal Implementation (TypeScript)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { readFileSync, readdirSync } from "fs";
import { parse } from "yaml";
import { join } from "path";

const server = new Server(
  { name: "prompt-catalog", version: "1.0.0" },
  { capabilities: { resources: {}, prompts: {} } }
);

const CATALOG_ROOT = process.env.CATALOG_ROOT || ".";

// List available resources
server.setRequestHandler("resources/list", async () => {
  const resources = [];
  const promptDirs = ["planning", "architecture", "development",
    "testing", "security", "deployment", "operations", "domains"];

  for (const dir of promptDirs) {
    const dirPath = join(CATALOG_ROOT, "prompts", dir);
    try {
      const files = readdirSync(dirPath).filter(f => f.endsWith(".yaml"));
      for (const file of files) {
        const content = readFileSync(join(dirPath, file), "utf-8");
        const prompt = parse(content);
        resources.push({
          uri: `prompt-catalog://prompts/${dir}/${prompt.id}`,
          name: prompt.title,
          description: prompt.description,
          mimeType: "text/yaml",
          metadata: {
            category: prompt.category,
            skill_level: prompt.skill_level,
            platforms: prompt.platforms,
            tags: prompt.tags
          }
        });
      }
    } catch (e) { /* directory may not exist */ }
  }

  return { resources };
});

// Read a specific resource
server.setRequestHandler("resources/read", async (request) => {
  const uri = request.params.uri;
  // Parse URI and read corresponding file
  // ... implementation
});

// List available prompt templates
server.setRequestHandler("prompts/list", async () => {
  // Parse all YAML files and extract variable definitions
  // Return as MCP prompt templates
  // ... implementation
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Integration with Existing MCP Hosts

Add to your MCP settings (e.g., `claude_desktop_config.json`):

**TypeScript / Node.js server:**

```json
{
  "mcpServers": {
    "prompt-catalog": {
      "command": "node",
      "args": ["path/to/prompt-catalog-server/index.js"],
      "env": {
        "CATALOG_ROOT": "/path/to/prompt-catalog"
      }
    }
  }
}
```

**Python server:**

```json
{
  "mcpServers": {
    "prompt-catalog": {
      "command": "python",
      "args": ["path/to/prompt-catalog-server/server.py"],
      "env": {
        "CATALOG_ROOT": "/path/to/prompt-catalog"
      }
    }
  }
}
```

### Minimal Implementation (Python)

```python
"""
Prompt Catalog MCP Server — Python implementation.

Requires:
    pip install mcp pyyaml
"""

import os
import re
from pathlib import Path

import yaml
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    Resource,
    TextContent,
)

CATALOG_ROOT = Path(os.environ.get("CATALOG_ROOT", "."))
PROMPT_DIRS = [
    "planning", "architecture", "development", "testing",
    "security", "deployment", "operations", "domains",
]

server = Server("prompt-catalog")


# ── Helpers ──────────────────────────────────────────────────────────

def _load_prompt(path: Path) -> dict:
    """Parse a YAML prompt file and return its contents."""
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _iter_prompts():
    """Yield (dir_name, path, parsed_dict) for every prompt YAML file."""
    for dir_name in PROMPT_DIRS:
        dir_path = CATALOG_ROOT / "prompts" / dir_name
        if not dir_path.is_dir():
            continue
        for file in sorted(dir_path.glob("*.yaml")):
            if file.name.startswith("_"):
                continue  # skip _template.yaml
            yield dir_name, file, _load_prompt(file)


def _iter_instructions():
    """Yield (scope, path) for every instruction Markdown file."""
    for scope in ("phases", "guardrails", "platforms"):
        scope_dir = CATALOG_ROOT / "instructions" / scope
        if not scope_dir.is_dir():
            continue
        for file in sorted(scope_dir.glob("*.instructions.md")):
            yield scope, file


def _extract_variables(prompt_text: str) -> list[str]:
    """Extract {{variable}} placeholders from a prompt string."""
    return list(dict.fromkeys(re.findall(r"\{\{(\w+)\}\}", prompt_text)))


# ── Resources ────────────────────────────────────────────────────────

@server.list_resources()
async def list_resources() -> list[Resource]:
    resources: list[Resource] = []

    # Prompt resources
    for dir_name, file, data in _iter_prompts():
        resources.append(
            Resource(
                uri=f"prompt-catalog://prompts/{dir_name}/{data['id']}",
                name=data["title"],
                description=data.get("description", ""),
                mimeType="text/yaml",
            )
        )

    # Instruction resources
    for scope, file in _iter_instructions():
        resources.append(
            Resource(
                uri=f"prompt-catalog://instructions/{scope}/{file.stem}",
                name=file.stem,
                description=f"{scope} instruction file",
                mimeType="text/markdown",
            )
        )

    return resources


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Return the raw file content for a given resource URI."""
    # prompt-catalog://prompts/{dir}/{id}
    if uri.startswith("prompt-catalog://prompts/"):
        parts = uri.replace("prompt-catalog://prompts/", "").split("/")
        dir_name, prompt_id = parts[0], parts[1]
        for _, file, data in _iter_prompts():
            if data["id"] == prompt_id:
                return file.read_text(encoding="utf-8")
        raise ValueError(f"Prompt not found: {prompt_id}")

    # prompt-catalog://instructions/{scope}/{stem}
    if uri.startswith("prompt-catalog://instructions/"):
        parts = uri.replace("prompt-catalog://instructions/", "").split("/")
        scope, stem = parts[0], parts[1]
        target = CATALOG_ROOT / "instructions" / scope / f"{stem}.md"
        if target.exists():
            return target.read_text(encoding="utf-8")
        raise ValueError(f"Instruction not found: {stem}")

    raise ValueError(f"Unknown URI scheme: {uri}")


# ── Prompt Templates ────────────────────────────────────────────────

@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    prompts: list[Prompt] = []

    for _, _, data in _iter_prompts():
        variables = data.get("variables", [])
        arguments = [
            PromptArgument(
                name=var["name"],
                description=var.get("description", ""),
                required=var.get("required", False),
            )
            for var in variables
        ]
        prompts.append(
            Prompt(
                name=data["id"].lower(),
                description=data.get("description", data["title"]),
                arguments=arguments,
            )
        )

    return prompts


@server.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None = None) -> GetPromptResult:
    """Fill in a prompt template with the supplied arguments."""
    for _, _, data in _iter_prompts():
        if data["id"].lower() == name:
            prompt_text = data.get("prompt", "")

            # Substitute {{variables}} with provided arguments
            if arguments:
                for key, value in arguments.items():
                    prompt_text = prompt_text.replace(f"{{{{{key}}}}}", value)

            return GetPromptResult(
                description=data.get("description", data["title"]),
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(type="text", text=prompt_text),
                    )
                ],
            )

    raise ValueError(f"Prompt not found: {name}")


# ── Filtering helpers (for advanced usage) ───────────────────────────

def filter_prompts(
    category: str | None = None,
    skill_level: str | None = None,
    platform: str | None = None,
    tag: str | None = None,
) -> list[dict]:
    """Return prompt metadata matching the given filters."""
    results = []
    skill_order = ["beginner", "intermediate", "advanced", "expert"]

    for _, _, data in _iter_prompts():
        if category and data.get("category") != category:
            continue
        if skill_level:
            max_idx = skill_order.index(skill_level)
            cur_idx = skill_order.index(data.get("skill_level", "expert"))
            if cur_idx > max_idx:
                continue
        if platform and platform not in data.get("platforms", []):
            continue
        if tag and tag not in data.get("tags", []):
            continue
        results.append(data)

    return results


# ── Entry point ──────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Instruction File Loading Strategy

Instruction files should be loaded contextually based on the task:

1. **Always load**: `guardrails/accuracy.instructions.md` (anti-hallucination)
2. **Load by phase**: Match SDLC phase instructions to the current task
3. **Load by platform**: Load platform instructions matching the target platform
4. **Load by domain**: Load domain-specific instructions when applicable
5. **Load by `load_with`**: Follow the `load_with` field in instruction frontmatter

### Recommended Loading Order

```
1. Guardrail instructions (accuracy, security)     ← Safety baseline
2. Platform instructions (for target platform)       ← Platform context
3. Phase instructions (for current SDLC phase)       ← Process guidance
4. Domain instructions (if domain-specific)          ← Domain expertise
5. Selected prompt template                          ← Specific task
```

## Contributing an MCP Server Implementation

If you build an MCP server for this catalog, we welcome contributions! See the main [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### Implementation Requirements

- Parse YAML prompt files according to `schema/prompt.schema.json`
- Parse instruction file frontmatter according to `schema/instruction.schema.json`
- Support filtering by category, skill_level, platform, and tags
- Handle `{{variable}}` extraction for prompt templates
- Respect `chain_position` for workflow sequencing

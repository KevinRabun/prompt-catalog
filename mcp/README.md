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

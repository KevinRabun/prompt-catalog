"""
Catalog loader — reads, parses, indexes, and filters the prompt catalog.

This module is the shared backend used by both the MCP server and the CLI.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

# ── Constants ────────────────────────────────────────────────────────

PROMPT_DIRS = [
    "planning",
    "architecture",
    "development",
    "testing",
    "security",
    "deployment",
    "operations",
    "domains",
]

INSTRUCTION_SCOPES = ["phases", "guardrails", "platforms"]

SKILL_ORDER = ["beginner", "intermediate", "advanced", "expert"]


# ── Data classes ─────────────────────────────────────────────────────


@dataclass
class PromptEntry:
    """A single prompt loaded from a YAML file."""

    id: str
    version: str
    title: str
    description: str
    category: str
    subcategory: str
    skill_level: str
    platforms: list[str]
    tags: list[str]
    prompt_text: str
    variables: list[dict]
    expected_output: str
    quality_criteria: list[str]
    anti_patterns: list[str]
    adversarial_tests: list[dict]
    related_prompts: list[str]
    chain_position: dict
    file_path: Path
    raw: dict  # full parsed YAML

    @classmethod
    def from_yaml(cls, path: Path) -> "PromptEntry":
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return cls(
            id=data["id"],
            version=data.get("version", "1.0.0"),
            title=data["title"],
            description=data.get("description", ""),
            category=data.get("category", ""),
            subcategory=data.get("subcategory", ""),
            skill_level=data.get("skill_level", "intermediate"),
            platforms=data.get("platforms", []),
            tags=data.get("tags", []),
            prompt_text=data.get("prompt", ""),
            variables=data.get("variables", []),
            expected_output=data.get("expected_output", ""),
            quality_criteria=data.get("quality_criteria", []),
            anti_patterns=data.get("anti_patterns", []),
            adversarial_tests=data.get("adversarial_tests", []),
            related_prompts=data.get("related_prompts", []),
            chain_position=data.get("chain_position", {}),
            file_path=path,
            raw=data,
        )

    def extract_variable_names(self) -> list[str]:
        """Return ordered unique {{variable}} names from the prompt text."""
        return list(dict.fromkeys(re.findall(r"\{\{(\w+)\}\}", self.prompt_text)))

    def render(self, arguments: dict[str, str] | None = None) -> str:
        """Substitute {{variables}} with supplied values."""
        text = self.prompt_text
        if arguments:
            for key, value in arguments.items():
                text = text.replace(f"{{{{{key}}}}}", value)
        return text


@dataclass
class InstructionEntry:
    """A single instruction file."""

    stem: str
    scope: str  # phases | guardrails | platforms
    file_path: Path
    name: str = ""
    description: str = ""

    @classmethod
    def from_path(cls, scope: str, path: Path) -> "InstructionEntry":
        # Parse YAML frontmatter for name/description
        text = path.read_text(encoding="utf-8")
        name = ""
        description = ""
        if text.startswith("---"):
            end = text.index("---", 3)
            fm = yaml.safe_load(text[3:end])
            if fm:
                name = fm.get("name", "")
                description = fm.get("description", "")
        return cls(
            stem=path.stem,
            scope=scope,
            file_path=path,
            name=name or path.stem,
            description=description,
        )


@dataclass
class StarterKit:
    """A pre-configured bundle of prompts and instructions."""

    id: str
    name: str
    description: str
    target_audience: str
    prompts: list[str]
    instructions: list[str]
    tags: list[str]
    raw: dict

    @classmethod
    def from_yaml(cls, path: Path) -> "StarterKit":
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            target_audience=data.get("target_audience", ""),
            prompts=data.get("prompts", []),
            instructions=data.get("instructions", []),
            tags=data.get("tags", []),
            raw=data,
        )


# ── Catalog ──────────────────────────────────────────────────────────


@dataclass
class Catalog:
    """Loaded, indexed prompt catalog."""

    root: Path
    prompts: dict[str, PromptEntry] = field(default_factory=dict)
    instructions: dict[str, InstructionEntry] = field(default_factory=dict)
    starter_kits: dict[str, StarterKit] = field(default_factory=dict)

    @classmethod
    def load(cls, root: str | Path) -> "Catalog":
        root = Path(root).resolve()
        cat = cls(root=root)

        # Load prompts
        for dir_name in PROMPT_DIRS:
            dir_path = root / "prompts" / dir_name
            if not dir_path.is_dir():
                continue
            for f in sorted(dir_path.glob("*.yaml")):
                if f.name.startswith("_"):
                    continue
                try:
                    entry = PromptEntry.from_yaml(f)
                    cat.prompts[entry.id] = entry
                except Exception as exc:
                    logger.warning("Skipping malformed prompt %s: %s", f, exc)

        # Load instructions
        for scope in INSTRUCTION_SCOPES:
            scope_dir = root / "instructions" / scope
            if not scope_dir.is_dir():
                continue
            for f in sorted(scope_dir.glob("*.instructions.md")):
                try:
                    entry = InstructionEntry.from_path(scope, f)
                    cat.instructions[entry.stem] = entry
                except Exception as exc:
                    logger.warning("Skipping malformed instruction %s: %s", f, exc)

        # Load starter kits
        kits_dir = root / "starter-kits"
        if kits_dir.is_dir():
            for f in sorted(kits_dir.glob("*.yaml")):
                try:
                    kit = StarterKit.from_yaml(f)
                    cat.starter_kits[kit.id] = kit
                except Exception as exc:
                    logger.warning("Skipping malformed starter kit %s: %s", f, exc)

        return cat

    # ── Filtering ────────────────────────────────────────────────────

    def filter_prompts(
        self,
        *,
        category: str | None = None,
        subcategory: str | None = None,
        skill_level: str | None = None,
        platform: str | None = None,
        tag: str | None = None,
        query: str | None = None,
    ) -> list[PromptEntry]:
        results = []
        for p in self.prompts.values():
            if category and p.category != category:
                continue
            if subcategory and p.subcategory != subcategory:
                continue
            if skill_level:
                max_idx = SKILL_ORDER.index(skill_level)
                cur_idx = SKILL_ORDER.index(p.skill_level)
                if cur_idx > max_idx:
                    continue
            if platform and platform not in p.platforms and "all" not in p.platforms:
                continue
            if tag and tag not in p.tags:
                continue
            if query:
                q = query.lower()
                searchable = f"{p.title} {p.description} {' '.join(p.tags)}".lower()
                if q not in searchable:
                    continue
            results.append(p)
        return results

    def get_chain(self, start_id: str) -> list[PromptEntry]:
        """Walk a prompt chain forward from the given prompt ID."""
        chain = []
        visited = set()
        current_id = start_id

        while current_id and current_id not in visited:
            visited.add(current_id)
            prompt = self.prompts.get(current_id)
            if not prompt:
                break
            chain.append(prompt)
            next_ids = prompt.chain_position.get("next", [])
            current_id = next_ids[0] if next_ids else None

        return chain

    def resolve_kit(self, kit_id: str) -> tuple[list[PromptEntry], list[InstructionEntry]]:
        """Resolve a starter kit into its constituent prompts and instructions."""
        kit = self.starter_kits.get(kit_id)
        if not kit:
            raise ValueError(f"Starter kit not found: {kit_id}")

        prompts = [self.prompts[pid] for pid in kit.prompts if pid in self.prompts]
        instructions = [
            self.instructions[iid]
            for iid in kit.instructions
            if iid in self.instructions
        ]
        return prompts, instructions

    def get_index(self) -> dict:
        """Load the master index.json if available."""
        index_path = self.root / "prompts" / "index.json"
        if index_path.exists():
            return json.loads(index_path.read_text(encoding="utf-8"))
        return {}

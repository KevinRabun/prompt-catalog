"""
Prompt Catalog Validator.

Validates prompt YAML files against the JSON schema, checks index.json
integrity, and verifies starter kit references.

Usage:
    prompt-catalog validate          # Validate everything
    prompt-catalog validate --prompts   # Prompts only
    prompt-catalog validate --index     # Index integrity only
    prompt-catalog validate --kits      # Starter kit references only
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from jsonschema import Draft7Validator, ValidationError

from .catalog import PROMPT_DIRS, INSTRUCTION_SCOPES


@dataclass
class Issue:
    """A single validation issue."""

    file: str
    message: str
    severity: str = "error"  # error | warning

    def __str__(self) -> str:
        icon = "✗" if self.severity == "error" else "⚠"
        return f"  {icon} {self.file}: {self.message}"


@dataclass
class ValidationResult:
    """Aggregated validation results."""

    issues: list[Issue] = field(default_factory=list)
    files_checked: int = 0
    files_passed: int = 0

    @property
    def ok(self) -> bool:
        return not any(i.severity == "error" for i in self.issues)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "warning")


def _load_schema(root: Path, name: str) -> dict | None:
    """Load a JSON schema file from the schema/ directory."""
    schema_path = root / "schema" / name
    if not schema_path.exists():
        return None
    return json.loads(schema_path.read_text(encoding="utf-8"))


def validate_prompts(root: Path) -> ValidationResult:
    """Validate all prompt YAML files against the prompt schema."""
    result = ValidationResult()

    schema = _load_schema(root, "prompt.schema.json")
    if not schema:
        result.issues.append(Issue("schema/prompt.schema.json", "Schema file not found"))
        return result

    validator = Draft7Validator(schema)

    for dir_name in PROMPT_DIRS:
        dir_path = root / "prompts" / dir_name
        if not dir_path.is_dir():
            continue

        for yaml_file in sorted(dir_path.glob("*.yaml")):
            result.files_checked += 1
            rel_path = str(yaml_file.relative_to(root))

            try:
                data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
            except yaml.YAMLError as e:
                result.issues.append(Issue(rel_path, f"YAML parse error: {e}"))
                continue

            if not isinstance(data, dict):
                result.issues.append(Issue(rel_path, "File does not contain a YAML mapping"))
                continue

            errors = list(validator.iter_errors(data))
            if errors:
                for err in errors:
                    path = ".".join(str(p) for p in err.absolute_path) or "(root)"
                    result.issues.append(Issue(rel_path, f"{path}: {err.message}"))
            else:
                result.files_passed += 1

            # Additional checks beyond JSON schema
            _check_prompt_extras(data, rel_path, result)

    return result


def _check_prompt_extras(data: dict, rel_path: str, result: ValidationResult) -> None:
    """Run additional validation checks beyond what the JSON schema covers."""
    prompt_text = data.get("prompt", "")
    variables = data.get("variables", [])

    # Check that all {{variables}} in the prompt have matching variable definitions
    import re
    used_vars = set(re.findall(r"\{\{(\w+)\}\}", prompt_text))
    defined_vars = {v["name"] for v in variables}

    undefined = used_vars - defined_vars
    if undefined:
        result.issues.append(Issue(
            rel_path,
            f"Variables used in prompt but not defined: {', '.join(sorted(undefined))}",
            severity="warning",
        ))

    unused = defined_vars - used_vars
    if unused:
        result.issues.append(Issue(
            rel_path,
            f"Variables defined but not used in prompt: {', '.join(sorted(unused))}",
            severity="warning",
        ))

    # Check that chain_position references valid IDs (collected later at index level)
    # Check that related_prompts has no self-references
    prompt_id = data.get("id", "")
    related = data.get("related_prompts", [])
    if prompt_id in related:
        result.issues.append(Issue(
            rel_path,
            f"Prompt references itself in related_prompts",
            severity="warning",
        ))


def validate_index(root: Path) -> ValidationResult:
    """Validate the master index.json file for integrity."""
    result = ValidationResult()
    index_path = root / "prompts" / "index.json"

    if not index_path.exists():
        result.issues.append(Issue("prompts/index.json", "Index file not found"))
        return result

    result.files_checked = 1

    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        result.issues.append(Issue("prompts/index.json", f"JSON parse error: {e}"))
        return result

    # Check that all prompt entries reference files that exist
    prompts = index.get("prompts", [])
    for entry in prompts:
        prompt_id = entry.get("id", "unknown")
        file_path = entry.get("file", "")
        if file_path:
            full_path = root / file_path
            if not full_path.exists():
                result.issues.append(Issue(
                    "prompts/index.json",
                    f"Prompt {prompt_id} references non-existent file: {file_path}",
                ))
        else:
            result.issues.append(Issue(
                "prompts/index.json",
                f"Prompt {prompt_id} has no file path",
            ))

    # Check that all instruction entries reference files that exist
    instructions = index.get("instructions", [])
    for entry in instructions:
        inst_id = entry.get("id", "unknown")
        file_path = entry.get("file", "")
        if file_path:
            full_path = root / file_path
            if not full_path.exists():
                result.issues.append(Issue(
                    "prompts/index.json",
                    f"Instruction {inst_id} references non-existent file: {file_path}",
                ))

    # Check that starter kit entries reference files that exist
    starter_kits = index.get("starter_kits", [])
    for entry in starter_kits:
        kit_id = entry.get("id", "unknown")
        file_path = entry.get("file", "")
        if file_path:
            full_path = root / file_path
            if not full_path.exists():
                result.issues.append(Issue(
                    "prompts/index.json",
                    f"Starter kit {kit_id} references non-existent file: {file_path}",
                ))

    # Verify prompt count matches
    stated_count = index.get("statistics", {}).get("total_prompts", 0)
    actual_count = len(prompts)
    if stated_count != actual_count:
        result.issues.append(Issue(
            "prompts/index.json",
            f"Statistics says {stated_count} prompts but index lists {actual_count}",
            severity="warning",
        ))

    # Check for duplicate prompt IDs
    prompt_ids = [p.get("id") for p in prompts]
    seen = set()
    for pid in prompt_ids:
        if pid in seen:
            result.issues.append(Issue(
                "prompts/index.json",
                f"Duplicate prompt ID in index: {pid}",
            ))
        seen.add(pid)

    # Cross-reference: every YAML file in prompts/ should be in the index
    index_files = {entry.get("file", "") for entry in prompts}
    for dir_name in PROMPT_DIRS:
        dir_path = root / "prompts" / dir_name
        if not dir_path.is_dir():
            continue
        for yaml_file in sorted(dir_path.glob("*.yaml")):
            rel = f"prompts/{dir_name}/{yaml_file.name}"
            if rel not in index_files:
                result.issues.append(Issue(
                    "prompts/index.json",
                    f"YAML file not listed in index: {rel}",
                    severity="warning",
                ))

    if not result.issues:
        result.files_passed = 1

    return result


def validate_kits(root: Path) -> ValidationResult:
    """Validate starter kit YAML files for reference integrity."""
    result = ValidationResult()
    kits_dir = root / "starter-kits"

    if not kits_dir.is_dir():
        result.issues.append(Issue("starter-kits/", "Starter kits directory not found"))
        return result

    # Load all available prompt IDs and instruction stems for cross-reference
    available_prompts = set()
    for dir_name in PROMPT_DIRS:
        dir_path = root / "prompts" / dir_name
        if not dir_path.is_dir():
            continue
        for yaml_file in dir_path.glob("*.yaml"):
            try:
                data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
                if data and "id" in data:
                    available_prompts.add(data["id"])
            except yaml.YAMLError as e:
                rel_prompt_path = str(yaml_file.relative_to(root))
                result.issues.append(Issue(rel_prompt_path, f"YAML parse error while scanning prompts: {e}"))

    available_instructions = set()
    for scope in INSTRUCTION_SCOPES:
        scope_dir = root / "instructions" / scope
        if not scope_dir.is_dir():
            continue
        for f in scope_dir.glob("*.instructions.md"):
            # Stem without .instructions.md → scope/stem_without_suffix
            stem = f.stem  # e.g., "accuracy.instructions"
            # The kit references use format like "guardrails/accuracy"
            clean_stem = stem.replace(".instructions", "")
            available_instructions.add(f"{scope}/{clean_stem}")

    for kit_file in sorted(kits_dir.glob("*.yaml")):
        if kit_file.name == "README.md":
            continue

        result.files_checked += 1
        rel_path = str(kit_file.relative_to(root))

        try:
            data = yaml.safe_load(kit_file.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            result.issues.append(Issue(rel_path, f"YAML parse error: {e}"))
            continue

        if not isinstance(data, dict):
            result.issues.append(Issue(rel_path, "File does not contain a YAML mapping"))
            continue

        # Required fields
        for field in ["id", "name", "description", "prompts", "instructions"]:
            if field not in data:
                result.issues.append(Issue(rel_path, f"Missing required field: {field}"))

        # Check prompt references
        kit_prompts = data.get("prompts", [])
        for pid in kit_prompts:
            # Strip inline comments from YAML (they're parsed as part of the string in flow style)
            clean_pid = pid.strip()
            if clean_pid not in available_prompts:
                result.issues.append(Issue(
                    rel_path,
                    f"References non-existent prompt: {clean_pid}",
                ))

        # Check instruction references
        kit_instructions = data.get("instructions", [])
        for iid in kit_instructions:
            clean_iid = iid.strip()
            if clean_iid not in available_instructions:
                result.issues.append(Issue(
                    rel_path,
                    f"References non-existent instruction: {clean_iid}",
                ))

        if not any(i.file == rel_path and i.severity == "error" for i in result.issues):
            result.files_passed += 1

    return result


def validate_instructions(root: Path) -> ValidationResult:
    """Validate that instruction files have valid frontmatter."""
    result = ValidationResult()

    for scope in INSTRUCTION_SCOPES:
        scope_dir = root / "instructions" / scope
        if not scope_dir.is_dir():
            continue

        for md_file in sorted(scope_dir.glob("*.instructions.md")):
            result.files_checked += 1
            rel_path = str(md_file.relative_to(root))

            text = md_file.read_text(encoding="utf-8")

            # Must start with YAML frontmatter
            if not text.startswith("---"):
                result.issues.append(Issue(
                    rel_path,
                    "Missing YAML frontmatter (must start with ---)",
                ))
                continue

            try:
                end = text.index("---", 3)
                fm = yaml.safe_load(text[3:end])
            except (ValueError, yaml.YAMLError) as e:
                result.issues.append(Issue(rel_path, f"Invalid frontmatter: {e}"))
                continue

            if not fm or not isinstance(fm, dict):
                result.issues.append(Issue(rel_path, "Frontmatter is empty or not a mapping"))
                continue

            # VS Code requires at least 'name' in frontmatter
            if "name" not in fm:
                result.issues.append(Issue(rel_path, "Frontmatter missing 'name' field"))

            if "description" not in fm:
                result.issues.append(Issue(
                    rel_path,
                    "Frontmatter missing 'description' field",
                    severity="warning",
                ))

            # Check body has actual content
            body = text[end + 3:].strip()
            if len(body) < 50:
                result.issues.append(Issue(
                    rel_path,
                    "Instruction body is too short (< 50 chars)",
                    severity="warning",
                ))

            if not any(i.file == rel_path and i.severity == "error" for i in result.issues):
                result.files_passed += 1

    return result


def validate_all(root: Path) -> dict[str, ValidationResult]:
    """Run all validation checks and return results by category."""
    return {
        "prompts": validate_prompts(root),
        "instructions": validate_instructions(root),
        "index": validate_index(root),
        "starter-kits": validate_kits(root),
    }

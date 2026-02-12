"""Tests for the prompt catalog validator."""

from __future__ import annotations

import json
from pathlib import Path

import yaml


# ── Prompt Validation ────────────────────────────────────────────────


class TestValidatePrompts:
    def test_valid_prompts_pass(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_prompts

        result = validate_prompts(catalog_root)
        assert result.ok
        assert result.files_checked == 2
        assert result.files_passed == 2
        assert result.error_count == 0

    def test_invalid_yaml_syntax(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_prompts

        bad = catalog_root / "prompts" / "planning" / "bad-yaml.yaml"
        bad.write_text("id: bad\n  broken: indent", encoding="utf-8")

        result = validate_prompts(catalog_root)
        assert not result.ok
        errors = [i for i in result.issues if "bad-yaml" in i.file and i.severity == "error"]
        assert len(errors) >= 1

    def test_missing_required_field(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_prompts

        incomplete = {"id": "incomplete", "name": "Incomplete Prompt"}
        (catalog_root / "prompts" / "planning" / "incomplete.yaml").write_text(
            yaml.dump(incomplete), encoding="utf-8"
        )

        result = validate_prompts(catalog_root)
        assert not result.ok
        errors = [i for i in result.issues if "incomplete" in i.file and i.severity == "error"]
        assert len(errors) >= 1

    def test_invalid_platform_value(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_prompts

        bad_plat = {
            "id": "bad-plat",
            "name": "Bad Platform",
            "category": "planning",
            "description": "x",
            "prompt": "Do something",
            "platforms": ["invalid-platform"],
        }
        (catalog_root / "prompts" / "planning" / "bad-plat.yaml").write_text(
            yaml.dump(bad_plat), encoding="utf-8"
        )

        result = validate_prompts(catalog_root)
        assert not result.ok
        errors = [i for i in result.issues if "bad-plat" in i.file and i.severity == "error"]
        assert len(errors) >= 1

    def test_undefined_variable_warning(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_prompts

        prompt = {
            "id": "undef-var",
            "name": "Undef Var",
            "category": "planning",
            "description": "x",
            "prompt": "Work on {{project}} and {{missing_var}}.",
            "variables": [
                {"name": "project", "description": "Project name"},
            ],
        }
        (catalog_root / "prompts" / "planning" / "undef-var.yaml").write_text(
            yaml.dump(prompt), encoding="utf-8"
        )

        result = validate_prompts(catalog_root)
        warnings = [i for i in result.issues if "undef-var" in i.file and i.severity == "warning"]
        assert any("missing_var" in w.message for w in warnings)

    def test_unused_variable_warning(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_prompts

        prompt = {
            "id": "unused-var",
            "name": "Unused Var",
            "category": "planning",
            "description": "x",
            "prompt": "Work on {{project}}.",
            "variables": [
                {"name": "project", "description": "Project name"},
                {"name": "orphan", "description": "Not used anywhere"},
            ],
        }
        (catalog_root / "prompts" / "planning" / "unused-var.yaml").write_text(
            yaml.dump(prompt), encoding="utf-8"
        )

        result = validate_prompts(catalog_root)
        warnings = [i for i in result.issues if "unused-var" in i.file and i.severity == "warning"]
        assert any("orphan" in w.message for w in warnings)

    def test_missing_schema_file(self, tmp_path: Path) -> None:
        from prompt_catalog_mcp.validator import validate_prompts

        # No schema dir at all
        result = validate_prompts(tmp_path)
        assert not result.ok
        assert any("Schema file not found" in i.message for i in result.issues)


# ── Instruction Validation ───────────────────────────────────────────


class TestValidateInstructions:
    def test_valid_instructions_pass(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_instructions

        result = validate_instructions(catalog_root)
        assert result.ok
        assert result.files_checked == 1
        assert result.files_passed == 1

    def test_missing_frontmatter(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_instructions

        bad = catalog_root / "instructions" / "guardrails" / "no-fm.instructions.md"
        bad.write_text("# No frontmatter\nJust content.", encoding="utf-8")

        result = validate_instructions(catalog_root)
        errors = [i for i in result.issues if "no-fm" in i.file]
        assert len(errors) >= 1

    def test_missing_name_field(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_instructions

        bad = catalog_root / "instructions" / "guardrails" / "no-name.instructions.md"
        bad.write_text("---\ndescription: test\n---\n\nContent here that is long enough.", encoding="utf-8")

        result = validate_instructions(catalog_root)
        errors = [i for i in result.issues if "no-name" in i.file and i.severity == "error"]
        assert len(errors) >= 1


# ── Index Validation ─────────────────────────────────────────────────


class TestValidateIndex:
    def test_valid_index_passes(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_index

        result = validate_index(catalog_root)
        assert result.ok

    def test_missing_referenced_file(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_index

        idx_path = catalog_root / "prompts" / "index.json"
        index = json.loads(idx_path.read_text())
        index["prompts"].append({
            "id": "ghost",
            "name": "Ghost Prompt",
            "file": "prompts/planning/ghost.yaml",
            "category": "planning",
        })
        idx_path.write_text(json.dumps(index))

        result = validate_index(catalog_root)
        assert not result.ok
        assert any("ghost" in i.message for i in result.issues)

    def test_duplicate_id(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_index

        idx_path = catalog_root / "prompts" / "index.json"
        index = json.loads(idx_path.read_text())
        # Duplicate an existing entry
        index["prompts"].append(index["prompts"][0])
        idx_path.write_text(json.dumps(index))

        result = validate_index(catalog_root)
        assert any("Duplicate" in i.message for i in result.issues)

    def test_count_mismatch_warning(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_index

        idx_path = catalog_root / "prompts" / "index.json"
        index = json.loads(idx_path.read_text())
        index["statistics"]["total_prompts"] = 999
        idx_path.write_text(json.dumps(index))

        result = validate_index(catalog_root)
        warnings = [i for i in result.issues if i.severity == "warning"]
        assert any("999" in w.message for w in warnings)

    def test_orphan_file_warning(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_index

        # Create a YAML file not in the index
        orphan = {
            "id": "orphan",
            "name": "Orphan Prompt",
            "category": "planning",
            "description": "x",
            "prompt": "x",
        }
        (catalog_root / "prompts" / "planning" / "orphan.yaml").write_text(
            yaml.dump(orphan), encoding="utf-8"
        )

        result = validate_index(catalog_root)
        warnings = [i for i in result.issues if i.severity == "warning" and "orphan" in i.message]
        assert len(warnings) >= 1


# ── Starter Kit Validation ───────────────────────────────────────────


class TestValidateKits:
    def test_valid_kit_passes(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_kits

        result = validate_kits(catalog_root)
        assert result.ok
        assert result.files_checked == 1
        assert result.files_passed == 1

    def test_bad_prompt_reference(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_kits

        bad_kit = {
            "id": "bad-kit",
            "name": "Bad Kit",
            "description": "Kit with bad refs",
            "prompts": ["nonexistent-prompt"],
            "instructions": ["guardrails/test-guard"],
            "tags": [],
        }
        (catalog_root / "starter-kits" / "bad-kit.yaml").write_text(
            yaml.dump(bad_kit), encoding="utf-8"
        )

        result = validate_kits(catalog_root)
        errors = [i for i in result.issues if "bad-kit" in i.file and "nonexistent" in i.message]
        assert len(errors) >= 1

    def test_bad_instruction_reference(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_kits

        bad_kit = {
            "id": "bad-inst-kit",
            "name": "Bad Instruction Kit",
            "description": "Kit with bad instruction ref",
            "prompts": ["test-prompt-1"],
            "instructions": ["guardrails/nonexistent"],
            "tags": [],
        }
        (catalog_root / "starter-kits" / "bad-inst-kit.yaml").write_text(
            yaml.dump(bad_kit), encoding="utf-8"
        )

        result = validate_kits(catalog_root)
        errors = [i for i in result.issues if "bad-inst-kit" in i.file and "nonexistent" in i.message]
        assert len(errors) >= 1

    def test_missing_required_field(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_kits

        bad_kit = {"id": "no-name-kit"}
        (catalog_root / "starter-kits" / "no-name-kit.yaml").write_text(
            yaml.dump(bad_kit), encoding="utf-8"
        )

        result = validate_kits(catalog_root)
        errors = [i for i in result.issues if "no-name-kit" in i.file]
        assert len(errors) >= 1


# ── Full Validation ──────────────────────────────────────────────────


class TestValidateAll:
    def test_validate_all_returns_all_categories(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_all

        results = validate_all(catalog_root)
        assert "prompts" in results
        assert "instructions" in results
        assert "index" in results
        assert "starter-kits" in results

    def test_clean_catalog_passes(self, catalog_root: Path) -> None:
        from prompt_catalog_mcp.validator import validate_all

        results = validate_all(catalog_root)
        total_errors = sum(r.error_count for r in results.values())
        assert total_errors == 0

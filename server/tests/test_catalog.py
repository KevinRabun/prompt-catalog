"""Tests for the catalog loader."""

from __future__ import annotations

from pathlib import Path

from prompt_catalog_mcp.catalog import Catalog, PromptEntry, InstructionEntry


class TestPromptEntry:
    def test_from_yaml(self, catalog_root: Path) -> None:
        path = catalog_root / "prompts" / "planning" / "test-prompt-1.yaml"
        entry = PromptEntry.from_yaml(path)
        assert entry.id == "test-prompt-1"
        assert entry.title == "Test Prompt"
        assert entry.category == "planning"
        assert "project_name" in [v["name"] for v in entry.variables]

    def test_render(self, catalog_root: Path) -> None:
        path = catalog_root / "prompts" / "planning" / "test-prompt-1.yaml"
        entry = PromptEntry.from_yaml(path)
        rendered = entry.render({"project_name": "Acme", "methodology": "scrum"})
        assert "Acme" in rendered
        assert "scrum" in rendered
        assert "{{" not in rendered

    def test_render_missing_var_left_as_placeholder(self, catalog_root: Path) -> None:
        path = catalog_root / "prompts" / "planning" / "test-prompt-1.yaml"
        entry = PromptEntry.from_yaml(path)
        rendered = entry.render({"project_name": "Acme"})
        assert "Acme" in rendered
        assert "{{methodology}}" in rendered  # unfilled var stays


class TestInstructionEntry:
    def test_from_path(self, catalog_root: Path) -> None:
        path = catalog_root / "instructions" / "guardrails" / "test-guard.instructions.md"
        entry = InstructionEntry.from_path("guardrails", path)
        assert entry.name == "Test Guardrail"


class TestCatalogLoad:
    def test_load(self, catalog_root: Path) -> None:
        catalog = Catalog.load(catalog_root)
        assert len(catalog.prompts) == 2
        assert "test-prompt-1" in catalog.prompts
        assert "test-prompt-2" in catalog.prompts

    def test_load_instructions(self, catalog_root: Path) -> None:
        catalog = Catalog.load(catalog_root)
        assert len(catalog.instructions) >= 1

    def test_load_starter_kits(self, catalog_root: Path) -> None:
        catalog = Catalog.load(catalog_root)
        assert "test-kit" in catalog.starter_kits


class TestCatalogFilter:
    def test_filter_by_category(self, catalog_root: Path) -> None:
        catalog = Catalog.load(catalog_root)
        results = catalog.filter_prompts(category="planning")
        assert len(results) == 2

    def test_filter_by_platform(self, catalog_root: Path) -> None:
        catalog = Catalog.load(catalog_root)
        results = catalog.filter_prompts(platform="web")
        # prompt-1 has "all" (matches everything), prompt-2 has "web"
        assert len(results) >= 1

    def test_filter_by_tag(self, catalog_root: Path) -> None:
        catalog = Catalog.load(catalog_root)
        results = catalog.filter_prompts(tag="planning")
        assert len(results) >= 1

    def test_filter_no_match(self, catalog_root: Path) -> None:
        catalog = Catalog.load(catalog_root)
        results = catalog.filter_prompts(category="security")
        assert len(results) == 0

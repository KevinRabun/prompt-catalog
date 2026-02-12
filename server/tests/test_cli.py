"""Tests for the CLI interface via Click's test runner."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from prompt_catalog_mcp.cli import main


@pytest.fixture
def cli_runner(catalog_root: Path):
    """Provide a Click test runner with CATALOG_ROOT set."""
    runner = CliRunner()
    env = {"CATALOG_ROOT": str(catalog_root)}
    return runner, env


class TestCLIList:
    def test_list_all(self, cli_runner) -> None:
        runner, env = cli_runner
        result = runner.invoke(main, ["list"], env=env)
        assert result.exit_code == 0
        assert "test-prompt-1" in result.output or "Test Prompt" in result.output

    def test_list_by_category(self, cli_runner) -> None:
        runner, env = cli_runner
        result = runner.invoke(main, ["list", "--category", "planning"], env=env)
        assert result.exit_code == 0

    def test_list_empty_category(self, cli_runner) -> None:
        runner, env = cli_runner
        result = runner.invoke(main, ["list", "--category", "security"], env=env)
        assert result.exit_code == 0


class TestCLISearch:
    def test_search_basic(self, cli_runner) -> None:
        runner, env = cli_runner
        result = runner.invoke(main, ["search", "plan"], env=env)
        assert result.exit_code == 0

    def test_search_no_results(self, cli_runner) -> None:
        runner, env = cli_runner
        result = runner.invoke(main, ["search", "zzzznonexistent"], env=env)
        assert result.exit_code == 0


class TestCLIShow:
    def test_show_valid(self, cli_runner) -> None:
        runner, env = cli_runner
        result = runner.invoke(main, ["show", "test-prompt-1"], env=env)
        assert result.exit_code == 0
        assert "test-prompt-1" in result.output or "Test Prompt" in result.output

    def test_show_invalid(self, cli_runner) -> None:
        runner, env = cli_runner
        result = runner.invoke(main, ["show", "nonexistent"], env=env)
        assert result.exit_code == 1  # CLI exits with code 1 for missing prompt


class TestCLIValidate:
    def test_validate_clean_catalog(self, cli_runner) -> None:
        runner, env = cli_runner
        result = runner.invoke(main, ["validate"], env=env)
        assert result.exit_code == 0
        assert "passed" in result.output.lower() or "✓" in result.output

    def test_validate_json_output(self, cli_runner) -> None:
        runner, env = cli_runner
        result = runner.invoke(main, ["validate", "--json-output"], env=env)
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "summary" in data
        assert data["summary"]["errors"] == 0

    def test_validate_prompts_only(self, cli_runner) -> None:
        runner, env = cli_runner
        result = runner.invoke(main, ["validate", "--prompts"], env=env)
        assert result.exit_code == 0

    def test_validate_index_only(self, cli_runner) -> None:
        runner, env = cli_runner
        result = runner.invoke(main, ["validate", "--index"], env=env)
        assert result.exit_code == 0

    def test_validate_kits_only(self, cli_runner) -> None:
        runner, env = cli_runner
        result = runner.invoke(main, ["validate", "--kits"], env=env)
        assert result.exit_code == 0

    def test_validate_fails_with_errors(self, cli_runner, catalog_root: Path) -> None:
        runner, env = cli_runner
        # Add a broken prompt
        broken = {"id": "broken", "name": "Broken"}
        (catalog_root / "prompts" / "planning" / "broken.yaml").write_text(
            __import__("yaml").dump(broken), encoding="utf-8"
        )
        result = runner.invoke(main, ["validate"], env=env)
        assert result.exit_code == 1


class TestCLIKit:
    def test_kit_list(self, cli_runner) -> None:
        runner, env = cli_runner
        result = runner.invoke(main, ["kit", "list"], env=env)
        assert result.exit_code == 0
        assert "test-kit" in result.output or "Test Kit" in result.output

    def test_kit_show(self, cli_runner) -> None:
        runner, env = cli_runner
        result = runner.invoke(main, ["kit", "show", "test-kit"], env=env)
        assert result.exit_code == 0


class TestCLIHelp:
    def test_main_help(self, cli_runner) -> None:
        runner, env = cli_runner
        result = runner.invoke(main, ["--help"], env=env)
        assert result.exit_code == 0
        assert "validate" in result.output

    def test_validate_help(self, cli_runner) -> None:
        runner, env = cli_runner
        result = runner.invoke(main, ["validate", "--help"], env=env)
        assert result.exit_code == 0

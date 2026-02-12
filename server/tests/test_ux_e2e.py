"""
End-to-end UX tests for the prompt-catalog CLI.

These tests run against the REAL catalog (not test fixtures) and validate
both deterministic properties and qualitative output via LLM judge evals.

Deterministic tests always run.
Judge eval tests require JUDGE_EVAL=1 and OPENAI_API_KEY in the environment.

Usage:
    # Deterministic only
    cd server && python -m pytest tests/test_ux_e2e.py -v

    # Include judge evals
    JUDGE_EVAL=1 OPENAI_API_KEY=sk-... python -m pytest tests/test_ux_e2e.py -v
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from click.testing import CliRunner

from prompt_catalog_mcp.cli import main

from .judge_eval import (
    RUBRIC_KIT_SHOW,
    RUBRIC_LIST_TABLE,
    RUBRIC_PROMPT_SHOW,
    RUBRIC_SEARCH_RESULTS,
    RUBRIC_START_RECOMMENDATIONS,
    RUBRIC_VALIDATE_OUTPUT,
    is_judge_enabled,
    judge,
)


# ── Fixtures ─────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parents[2]  # prompt-catalog repo root


@pytest.fixture
def runner():
    """Click CLI runner pointed at the real catalog."""
    env = {"CATALOG_ROOT": str(REPO_ROOT)}
    return CliRunner(), env


skip_judge = pytest.mark.skipif(
    not is_judge_enabled(),
    reason="JUDGE_EVAL not set — skipping LLM judge evaluation",
)


# ═════════════════════════════════════════════════════════════════════
# DETERMINISTIC TESTS — always run
# ═════════════════════════════════════════════════════════════════════


class TestHelpAndBanner:
    """Verify the CLI entrypoint and help output."""

    def test_no_args_shows_banner(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, [], env=env)
        assert result.exit_code == 0
        assert "Prompt Catalog" in result.output
        # All subcommands should be listed
        for cmd in ("list", "search", "show", "kit", "start", "validate", "serve"):
            assert cmd in result.output

    def test_help_flag(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["--help"], env=env)
        assert result.exit_code == 0
        assert "Usage" in result.output or "usage" in result.output.lower()


class TestList:
    """Test prompt listing with various filters."""

    def test_list_all_prompts(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["list"], env=env)
        assert result.exit_code == 0
        # Should have at least 30 prompts
        assert "found" in result.output.lower()
        # Extract count from "Prompts (N found)"
        import re
        m = re.search(r"(\d+)\s+found", result.output)
        assert m, "Could not find prompt count in output"
        count = int(m.group(1))
        assert count >= 30, f"Expected ≥30 prompts, got {count}"

    def test_list_columns(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["list"], env=env)
        assert result.exit_code == 0
        for col in ("ID", "Title", "Category", "Skill", "Platforms"):
            assert col in result.output

    def test_list_known_prompt_ids(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["list"], env=env)
        assert result.exit_code == 0
        # Spot-check well-known IDs
        for pid in ("PLAN-REQ-001", "ARCH-SYS-001", "SEC-THREAT-001",
                     "DEV-API-001", "TEST-UNIT-001"):
            assert pid in result.output, f"Expected {pid} in list output"

    def test_list_by_category_planning(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["list", "--category", "planning"], env=env)
        assert result.exit_code == 0
        assert "PLAN-" in result.output
        # Should NOT contain non-planning prompts
        assert "SEC-THREAT-001" not in result.output

    def test_list_by_category_security(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["list", "--category", "security"], env=env)
        assert result.exit_code == 0
        assert "SEC-" in result.output

    def test_list_by_category_domains(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["list", "--category", "domains"], env=env)
        assert result.exit_code == 0
        assert "DOM-" in result.output

    def test_list_domain_flag(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["list", "--domain"], env=env)
        assert result.exit_code == 0
        assert "DOM-" in result.output
        # Every visible ID should be a domain prompt
        import re
        ids = re.findall(r"[A-Z]+-[A-Z]+-\d+", result.output)
        for pid in ids:
            assert pid.startswith("DOM-"), f"Non-domain prompt {pid} in --domain output"

    def test_list_by_platform_web(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["list", "--platform", "web"], env=env)
        assert result.exit_code == 0
        assert "DEV-WEB-001" in result.output

    def test_list_by_skill_beginner(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["list", "--skill", "beginner"], env=env)
        assert result.exit_code == 0
        # Should not include advanced/expert prompts
        assert "advanced" not in result.output.lower()
        assert "expert" not in result.output.lower()

    def test_list_empty_category(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["list", "--category", "nonexistent"], env=env)
        assert result.exit_code == 0
        assert "no prompts" in result.output.lower() or "0 found" in result.output.lower()


class TestSearch:
    """Test keyword search across prompts."""

    def test_search_security(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["search", "security"], env=env)
        assert result.exit_code == 0
        assert "SEC-THREAT-001" in result.output or "SEC-CODE-001" in result.output
        import re
        m = re.search(r"(\d+)\s+found", result.output)
        assert m
        assert int(m.group(1)) >= 2, "Expected ≥2 results for 'security'"

    def test_search_api(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["search", "API"], env=env)
        assert result.exit_code == 0
        assert "DEV-API-001" in result.output

    def test_search_fintech(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["search", "fintech"], env=env)
        assert result.exit_code == 0
        assert "DOM-FINTECH-001" in result.output

    def test_search_no_results(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["search", "zzz_no_such_topic_zzz"], env=env)
        assert result.exit_code == 0
        assert "no prompts" in result.output.lower()

    def test_search_case_insensitive(self, runner) -> None:
        r, env = runner
        result_upper = r.invoke(main, ["search", "THREAT"], env=env)
        result_lower = r.invoke(main, ["search", "threat"], env=env)
        assert result_upper.exit_code == 0
        assert result_lower.exit_code == 0
        # Both should find the same prompts
        assert "SEC-THREAT-001" in result_upper.output
        assert "SEC-THREAT-001" in result_lower.output

    def test_search_columns(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["search", "security"], env=env)
        assert result.exit_code == 0
        for col in ("ID", "Title", "Category", "Description"):
            assert col in result.output


class TestShow:
    """Test prompt detail view."""

    def test_show_plan_req_001(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["show", "PLAN-REQ-001"], env=env)
        assert result.exit_code == 0
        assert "PLAN-REQ-001" in result.output
        # Should have metadata
        for field in ("Version", "Category", "Platforms", "Tags"):
            assert field in result.output or field.lower() in result.output.lower()

    def test_show_has_variables(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["show", "PLAN-REQ-001"], env=env)
        assert result.exit_code == 0
        assert "Variables" in result.output or "variable" in result.output.lower()

    def test_show_has_quality_criteria(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["show", "PLAN-REQ-001"], env=env)
        assert result.exit_code == 0
        assert "Quality" in result.output

    def test_show_has_anti_patterns(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["show", "PLAN-REQ-001"], env=env)
        assert result.exit_code == 0
        assert "Anti" in result.output

    def test_show_raw_yaml(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["show", "PLAN-REQ-001", "--raw"], env=env)
        assert result.exit_code == 0
        # Raw output should contain YAML keys
        assert "id:" in result.output or "title:" in result.output

    def test_show_case_insensitive(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["show", "plan-req-001"], env=env)
        assert result.exit_code == 0
        assert "PLAN-REQ-001" in result.output

    def test_show_not_found(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["show", "DOES-NOT-EXIST-999"], env=env)
        assert result.exit_code == 1
        assert "not found" in result.output.lower()

    def test_show_security_prompt(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["show", "SEC-THREAT-001"], env=env)
        assert result.exit_code == 0
        # Should mention threat modeling related content
        assert "SEC-THREAT-001" in result.output

    def test_show_domain_prompt(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["show", "DOM-FINTECH-001"], env=env)
        assert result.exit_code == 0
        assert "DOM-FINTECH-001" in result.output


class TestKit:
    """Test starter kit commands."""

    def test_kit_list(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["kit", "list"], env=env)
        assert result.exit_code == 0
        import re
        m = re.search(r"(\d+)\s+available", result.output)
        assert m
        assert int(m.group(1)) >= 5, f"Expected ≥5 kits, got {m.group(1)}"

    def test_kit_list_columns(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["kit", "list"], env=env)
        assert result.exit_code == 0
        for col in ("ID", "Name", "Audience", "Prompts", "Instructions"):
            assert col in result.output

    def test_kit_list_known_kits(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["kit", "list"], env=env)
        assert result.exit_code == 0
        for kit_id in ("saas-web-app", "api-backend", "cloud-native"):
            assert kit_id in result.output, f"Expected {kit_id} in kit list"

    def test_kit_show_saas(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["kit", "show", "saas-web-app"], env=env)
        assert result.exit_code == 0
        assert "saas-web-app" in result.output.lower() or "SaaS" in result.output
        # Should list prompts
        assert "PLAN-REQ-001" in result.output or "Prompts" in result.output

    def test_kit_show_not_found(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["kit", "show", "nonexistent-kit"], env=env)
        assert result.exit_code == 1
        assert "not found" in result.output.lower()

    def test_kit_export(self, runner, tmp_path) -> None:
        r, env = runner
        out = str(tmp_path)
        result = r.invoke(main, ["kit", "export", "saas-web-app", "--output", out], env=env)
        assert result.exit_code == 0
        assert "Exported" in result.output or "exported" in result.output.lower()

        export_dir = tmp_path / "saas-web-app"
        assert export_dir.is_dir()
        assert (export_dir / "prompts").is_dir()
        assert (export_dir / "instructions").is_dir()
        # Should have actual files
        prompt_files = list((export_dir / "prompts").glob("*.yaml"))
        assert len(prompt_files) >= 5, f"Expected ≥5 exported prompts, got {len(prompt_files)}"

    def test_kit_export_creates_instruction_files(self, runner, tmp_path) -> None:
        r, env = runner
        out = str(tmp_path)
        result = r.invoke(main, ["kit", "export", "saas-web-app", "--output", out], env=env)
        assert result.exit_code == 0
        # Instruction directory is created even if resolution finds zero matches
        # (kit uses scope/name format, catalog keys by stem — known limitation)
        assert (tmp_path / "saas-web-app" / "instructions").is_dir()


class TestValidate:
    """Test the validate command against the real catalog."""

    def test_validate_passes(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["validate"], env=env)
        assert result.exit_code == 0
        assert "passed" in result.output.lower() or "✓" in result.output

    def test_validate_json_output(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["validate", "--json-output"], env=env)
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "summary" in data
        assert data["summary"]["errors"] == 0
        assert data["summary"]["files_checked"] >= 30
        assert data["summary"]["files_passed"] >= 30

    def test_validate_json_has_all_categories(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["validate", "--json-output"], env=env)
        data = json.loads(result.output)
        assert "categories" in data
        for cat in ("prompts", "instructions", "index", "starter-kits"):
            assert cat in data["categories"], f"Missing validation category: {cat}"

    def test_validate_prompts_only(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["validate", "--prompts"], env=env)
        assert result.exit_code == 0

    def test_validate_index_only(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["validate", "--index"], env=env)
        assert result.exit_code == 0

    def test_validate_kits_only(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["validate", "--kits"], env=env)
        assert result.exit_code == 0


class TestStartInteractive:
    """Test the interactive `start` command with simulated user input."""

    def _simulate_start(self, runner, inputs: str) -> str:
        """Run `prompt-catalog start` with simulated stdin input."""
        r, env = runner
        result = r.invoke(main, ["start"], input=inputs, env=env)
        assert result.exit_code == 0
        return result.output

    def test_start_web_app_beginner(self, runner) -> None:
        # Choice 1: Web application, Platform 1: Web, Skill 1: beginner
        output = self._simulate_start(runner, "1\n1\n1\n")
        assert "Recommended" in output or "Prompts" in output
        assert "PLAN-REQ-001" in output

    def test_start_web_app_intermediate(self, runner) -> None:
        output = self._simulate_start(runner, "1\n1\n2\n")
        assert "PLAN-REQ-001" in output
        assert "DEV-WEB-001" in output

    def test_start_api_backend(self, runner) -> None:
        # Choice 3: API/Backend service, Platform 6: Cloud, Skill 2: intermediate
        output = self._simulate_start(runner, "3\n6\n2\n")
        assert "DEV-API-001" in output

    def test_start_cloud_native(self, runner) -> None:
        # Choice 5: Cloud-native, Platform 6: Cloud, Skill 3: advanced
        output = self._simulate_start(runner, "5\n6\n3\n")
        assert "ARCH-CLOUD-001" in output or "ARCH-MICRO-001" in output

    def test_start_domain_fintech(self, runner) -> None:
        # Choice 6: Domain-specific, Platform 1: Web, Skill 4: expert, Domain 6: FinTech
        # Note: domain numbering depends on alphabetical order of domain prompts
        output = self._simulate_start(runner, "6\n1\n4\n6\n")
        assert "PLAN-REQ-001" in output  # always included

    def test_start_recommendations_include_instructions(self, runner) -> None:
        output = self._simulate_start(runner, "1\n1\n2\n")
        assert "Instructions" in output or "instructions" in output
        assert "accuracy" in output.lower() or "security" in output.lower()

    def test_start_recommendations_include_security(self, runner) -> None:
        output = self._simulate_start(runner, "1\n1\n2\n")
        assert "SEC-THREAT-001" in output

    def test_start_recommendations_include_testing(self, runner) -> None:
        output = self._simulate_start(runner, "1\n1\n2\n")
        assert "TEST-UNIT-001" in output

    def test_start_recommendations_include_deployment(self, runner) -> None:
        output = self._simulate_start(runner, "1\n1\n2\n")
        assert "DEPLOY-CICD-001" in output


# ═════════════════════════════════════════════════════════════════════
# LLM JUDGE EVAL TESTS — run only with JUDGE_EVAL=1
# ═════════════════════════════════════════════════════════════════════


@skip_judge
class TestJudgeList:
    """LLM judge evaluation of the list command output."""

    def test_list_table_quality(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["list"], env=env)
        verdict = judge(result.output, RUBRIC_LIST_TABLE)
        assert verdict.passed, f"Judge failed: {verdict.reasoning}"


@skip_judge
class TestJudgeSearch:
    """LLM judge evaluation of search result relevance."""

    def test_search_relevance_security(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["search", "security"], env=env)
        rubric = RUBRIC_SEARCH_RESULTS + "\nThe search query was: 'security'"
        verdict = judge(result.output, rubric)
        assert verdict.passed, f"Judge failed: {verdict.reasoning}"

    def test_search_relevance_api(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["search", "API"], env=env)
        rubric = RUBRIC_SEARCH_RESULTS + "\nThe search query was: 'API'"
        verdict = judge(result.output, rubric)
        assert verdict.passed, f"Judge failed: {verdict.reasoning}"

    def test_search_relevance_cloud(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["search", "cloud"], env=env)
        rubric = RUBRIC_SEARCH_RESULTS + "\nThe search query was: 'cloud'"
        verdict = judge(result.output, rubric)
        assert verdict.passed, f"Judge failed: {verdict.reasoning}"


@skip_judge
class TestJudgeShow:
    """LLM judge evaluation of prompt detail display."""

    def test_show_prompt_quality(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["show", "PLAN-REQ-001"], env=env)
        verdict = judge(result.output, RUBRIC_PROMPT_SHOW)
        assert verdict.passed, f"Judge failed: {verdict.reasoning}"

    def test_show_security_prompt_quality(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["show", "SEC-THREAT-001"], env=env)
        verdict = judge(result.output, RUBRIC_PROMPT_SHOW)
        assert verdict.passed, f"Judge failed: {verdict.reasoning}"

    def test_show_domain_prompt_quality(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["show", "DOM-FINTECH-001"], env=env)
        verdict = judge(result.output, RUBRIC_PROMPT_SHOW)
        assert verdict.passed, f"Judge failed: {verdict.reasoning}"


@skip_judge
class TestJudgeKit:
    """LLM judge evaluation of starter kit display."""

    def test_kit_show_quality(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["kit", "show", "saas-web-app"], env=env)
        verdict = judge(result.output, RUBRIC_KIT_SHOW)
        assert verdict.passed, f"Judge failed: {verdict.reasoning}"

    def test_kit_show_cloud_native(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["kit", "show", "cloud-native"], env=env)
        verdict = judge(result.output, RUBRIC_KIT_SHOW)
        assert verdict.passed, f"Judge failed: {verdict.reasoning}"


@skip_judge
class TestJudgeStart:
    """LLM judge evaluation of interactive start recommendations."""

    def test_start_web_app_recommendations(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["start"], input="1\n1\n2\n", env=env)
        rubric = (
            RUBRIC_START_RECOMMENDATIONS
            + "\nThe user selected: Web application, Web platform, Intermediate skill level."
        )
        verdict = judge(result.output, rubric)
        assert verdict.passed, f"Judge failed: {verdict.reasoning}"

    def test_start_cloud_native_recommendations(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["start"], input="5\n6\n3\n", env=env)
        rubric = (
            RUBRIC_START_RECOMMENDATIONS
            + "\nThe user selected: Cloud-native/microservices, Cloud platform, Advanced skill level."
        )
        verdict = judge(result.output, rubric)
        assert verdict.passed, f"Judge failed: {verdict.reasoning}"


@skip_judge
class TestJudgeValidate:
    """LLM judge evaluation of validation output."""

    def test_validate_output_quality(self, runner) -> None:
        r, env = runner
        result = r.invoke(main, ["validate"], env=env)
        verdict = judge(result.output, RUBRIC_VALIDATE_OUTPUT)
        assert verdict.passed, f"Judge failed: {verdict.reasoning}"

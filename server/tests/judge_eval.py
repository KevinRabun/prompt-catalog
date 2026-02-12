"""
LLM Judge Evaluator — qualitative assessment of CLI outputs.

Gated behind the JUDGE_EVAL environment variable. When JUDGE_EVAL is not set,
all judge tests are automatically skipped.

Configure the LLM backend via environment variables:
    JUDGE_EVAL=1                     Enable judge evals
    JUDGE_MODEL=gpt-4o               Model name   (default: gpt-4o)
    OPENAI_API_KEY=sk-...            OpenAI API key

The evaluator sends CLI output + a rubric to the LLM and expects a JSON
response with {"pass": true/false, "reasoning": "..."}.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass


# ── Helpers ──────────────────────────────────────────────────────────

def is_judge_enabled() -> bool:
    return os.environ.get("JUDGE_EVAL", "").strip() in ("1", "true", "yes")


@dataclass
class JudgeVerdict:
    passed: bool
    reasoning: str
    rubric: str
    raw_response: str = ""


# ── System prompt ────────────────────────────────────────────────────

SYSTEM_PROMPT = """\
You are a strict QA evaluator for a developer-tools CLI called "prompt-catalog".
You will be given:
  1. A RUBRIC describing what the output MUST satisfy.
  2. The actual CLI OUTPUT to evaluate.

Respond with ONLY a single JSON object (no markdown fences):
{"pass": true, "reasoning": "One-sentence explanation"}
or
{"pass": false, "reasoning": "What is wrong and why it fails the rubric"}
"""


# ── Core judge function ─────────────────────────────────────────────

def judge(output: str, rubric: str, *, model: str | None = None) -> JudgeVerdict:
    """
    Send *output* to an LLM judge with *rubric* and return a verdict.

    Raises ImportError if openai is not installed.
    Raises RuntimeError if the LLM returns something unparseable.
    """
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise ImportError(
            "openai package is required for judge evals. "
            "Install with: pip install openai"
        ) from exc

    model = model or os.environ.get("JUDGE_MODEL", "gpt-4o")
    client = OpenAI()  # uses OPENAI_API_KEY from env

    user_message = (
        f"## RUBRIC\n{rubric}\n\n"
        f"## CLI OUTPUT\n```\n{output[:8000]}\n```"
    )

    response = client.chat.completions.create(
        model=model,
        temperature=0.0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content or ""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Judge returned non-JSON: {raw}") from exc

    return JudgeVerdict(
        passed=bool(data.get("pass", False)),
        reasoning=data.get("reasoning", ""),
        rubric=rubric,
        raw_response=raw,
    )


# ── Pre-built rubrics ───────────────────────────────────────────────

RUBRIC_PROMPT_SHOW = """\
The output should display a single prompt entry with ALL of the following:
1. A prompt ID in the format XXX-YYY-NNN (e.g., PLAN-REQ-001)
2. A descriptive title
3. Metadata: version, skill level, category, platforms, tags
4. A description of what the prompt does
5. A variables table with name, required, description, and example columns
6. Quality criteria (a checklist of what good output looks like)
7. Anti-patterns (what to avoid)
The output should be well-structured and readable for a developer."""

RUBRIC_KIT_SHOW = """\
The output should display a starter kit with ALL of the following:
1. A kit name and ID
2. Target audience description
3. A list of included prompts (by ID and title), covering multiple SDLC phases
4. A list of instruction files to load
5. The kit should represent a coherent, complete workflow — not random prompts
The overall presentation should help a developer understand what the kit
provides and how to use it."""

RUBRIC_SEARCH_RESULTS = """\
The output should show search results that are RELEVANT to the search query.
1. Results should be displayed in a table with ID, title, category, description
2. Each result must plausibly relate to the search query
3. There should be at least 1 result
4. No unrelated or random prompts should appear
The results should help a developer find what they searched for."""

RUBRIC_START_RECOMMENDATIONS = """\
The output should show a guided recommendation workflow that includes:
1. A recommended prompt stack (list of prompt IDs with titles)
2. Recommended instruction files to load
3. A matching starter kit suggestion (if applicable)
4. The prompts should span multiple SDLC phases (planning, architecture,
   development, testing, security, deployment, operations)
5. The recommendations should be coherent and appropriate for the project type
The output should make a developer confident about which prompts to use."""

RUBRIC_LIST_TABLE = """\
The output should display a well-formatted table of prompts with:
1. Columns for ID, Title, Category, Skill level, and Platforms
2. Each row should represent a distinct prompt
3. IDs should follow the format XXX-YYY-NNN
4. Categories should be standard SDLC categories
5. The table should have at least 30 rows
6. The table should be readable and professionally formatted."""

RUBRIC_VALIDATE_OUTPUT = """\
The output should display validation results that include:
1. Category-by-category results (prompts, instructions, index, starter-kits)
2. Pass/fail counts for each category
3. A summary line indicating overall pass or fail
4. If passing, a green checkmark or success indicator
The output should give a developer confidence that the catalog is well-formed."""

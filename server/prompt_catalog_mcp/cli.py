"""
Prompt Catalog CLI.

Usage:
    prompt-catalog list [--category CAT] [--platform PLAT] [--skill LEVEL] [--tag TAG]
    prompt-catalog search QUERY
    prompt-catalog show PROMPT_ID
    prompt-catalog kit list
    prompt-catalog kit show KIT_ID
    prompt-catalog kit export KIT_ID [--output DIR]
    prompt-catalog start                     # Interactive guided mode
    prompt-catalog serve                     # Start MCP server
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt as RichPrompt
from rich.syntax import Syntax

from .catalog import Catalog, SKILL_ORDER

console = Console()


def _find_catalog_root() -> Path:
    """Walk upward from CWD to find the prompt-catalog root (has prompts/ and instructions/)."""
    env_root = os.environ.get("CATALOG_ROOT")
    if env_root:
        return Path(env_root).resolve()

    # Check if we're inside the prompt-catalog repo
    cwd = Path.cwd().resolve()
    for p in [cwd, *cwd.parents]:
        if (p / "prompts" / "index.json").exists() and (p / "instructions").is_dir():
            return p
        # Stop at filesystem root
        if p == p.parent:
            break

    # Default to cwd
    return cwd


def _load_catalog() -> Catalog:
    root = _find_catalog_root()
    return Catalog.load(root)


# ── Main Group ───────────────────────────────────────────────────────


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """Prompt Catalog — AI-assisted software development prompt library."""
    if ctx.invoked_subcommand is None:
        console.print(
            Panel(
                "[bold]Prompt Catalog[/bold] — open-source prompt library for AI-assisted development\n\n"
                "Commands:\n"
                "  [cyan]list[/cyan]      List all prompts (with optional filters)\n"
                "  [cyan]search[/cyan]    Search prompts by keyword\n"
                "  [cyan]show[/cyan]      Show full prompt details\n"
                "  [cyan]kit[/cyan]       Manage starter kits\n"
                "  [cyan]start[/cyan]     Interactive guided mode\n"
                "  [cyan]validate[/cyan]  Validate prompts, instructions, and index\n"
                "  [cyan]serve[/cyan]     Start MCP server\n\n"
                "Run [cyan]prompt-catalog COMMAND --help[/cyan] for details.",
                title="prompt-catalog",
                border_style="blue",
            )
        )


# ── list ─────────────────────────────────────────────────────────────


@main.command("list")
@click.option("--category", "-c", help="Filter by category (planning, architecture, development, etc.)")
@click.option("--platform", "-p", help="Filter by platform (web, windows, linux, android, ios, cloud)")
@click.option("--skill", "-s", help="Max skill level (beginner, intermediate, advanced, expert)")
@click.option("--tag", "-t", help="Filter by tag")
@click.option("--domain", "-d", is_flag=True, help="Show only domain prompts")
def list_prompts(category, platform, skill, tag, domain):
    """List prompts with optional filtering."""
    catalog = _load_catalog()

    if domain:
        category = "domains"

    results = catalog.filter_prompts(
        category=category,
        skill_level=skill,
        platform=platform,
        tag=tag,
    )

    if not results:
        console.print("[yellow]No prompts match your filters.[/yellow]")
        return

    table = Table(title=f"Prompts ({len(results)} found)", show_lines=False)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="white")
    table.add_column("Category", style="green")
    table.add_column("Skill", style="yellow")
    table.add_column("Platforms", style="dim")

    for p in sorted(results, key=lambda x: x.id):
        platforms = ", ".join(p.platforms[:3])
        if len(p.platforms) > 3:
            platforms += "…"
        table.add_row(p.id, p.title, p.category, p.skill_level, platforms)

    console.print(table)


# ── search ───────────────────────────────────────────────────────────


@main.command("search")
@click.argument("query")
def search_prompts(query):
    """Search prompts by keyword in title, description, and tags."""
    catalog = _load_catalog()
    results = catalog.filter_prompts(query=query)

    if not results:
        console.print(f"[yellow]No prompts match '{query}'.[/yellow]")
        return

    table = Table(title=f"Search results for '{query}' ({len(results)} found)")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="white")
    table.add_column("Category", style="green")
    table.add_column("Description", style="dim", max_width=50)

    for p in results:
        desc = p.description[:50] + "…" if len(p.description) > 50 else p.description
        table.add_row(p.id, p.title, p.category, desc)

    console.print(table)


# ── show ─────────────────────────────────────────────────────────────


@main.command("show")
@click.argument("prompt_id")
@click.option("--raw", is_flag=True, help="Show raw YAML content")
def show_prompt(prompt_id, raw):
    """Show full details for a specific prompt."""
    catalog = _load_catalog()

    # Case-insensitive match
    entry = None
    for p in catalog.prompts.values():
        if p.id.lower() == prompt_id.lower():
            entry = p
            break

    if not entry:
        console.print(f"[red]Prompt not found: {prompt_id}[/red]")
        sys.exit(1)

    if raw:
        content = entry.file_path.read_text(encoding="utf-8")
        console.print(Syntax(content, "yaml", theme="monokai", line_numbers=True))
        return

    # Rich display
    console.print(Panel(f"[bold]{entry.title}[/bold]", subtitle=entry.id, border_style="cyan"))
    console.print(f"[dim]Version:[/dim] {entry.version}  [dim]Skill:[/dim] {entry.skill_level}  [dim]Category:[/dim] {entry.category}/{entry.subcategory}")
    console.print(f"[dim]Platforms:[/dim] {', '.join(entry.platforms)}")
    console.print(f"[dim]Tags:[/dim] {', '.join(entry.tags)}")
    console.print()
    console.print(f"[bold]Description:[/bold] {entry.description}")
    console.print()

    # Variables
    if entry.variables:
        var_table = Table(title="Variables", show_lines=True)
        var_table.add_column("Name", style="cyan")
        var_table.add_column("Required", style="yellow")
        var_table.add_column("Description")
        var_table.add_column("Examples", style="dim", max_width=40)
        for v in entry.variables:
            examples = ", ".join(v.get("examples", [])[:2])
            var_table.add_row(
                v["name"],
                "✓" if v.get("required") else "",
                v.get("description", ""),
                examples,
            )
        console.print(var_table)
        console.print()

    # Quality criteria
    if entry.quality_criteria:
        console.print("[bold green]Quality Criteria:[/bold green]")
        for c in entry.quality_criteria:
            console.print(f"  [green]✓[/green] {c}")
        console.print()

    # Anti-patterns
    if entry.anti_patterns:
        console.print("[bold red]Anti-Patterns:[/bold red]")
        for a in entry.anti_patterns:
            console.print(f"  [red]✗[/red] {a}")
        console.print()

    # Related & chain
    if entry.related_prompts:
        console.print(f"[dim]Related:[/dim] {', '.join(entry.related_prompts)}")
    if entry.chain_position:
        prev = entry.chain_position.get("previous", [])
        nxt = entry.chain_position.get("next", [])
        if prev:
            console.print(f"[dim]← Previous:[/dim] {', '.join(prev)}")
        if nxt:
            console.print(f"[dim]→ Next:[/dim] {', '.join(nxt)}")


# ── kit ──────────────────────────────────────────────────────────────


@main.group("kit")
def kit_group():
    """Manage opinionated starter kits."""
    pass


@kit_group.command("list")
def kit_list():
    """List all available starter kits."""
    catalog = _load_catalog()

    if not catalog.starter_kits:
        console.print("[yellow]No starter kits found.[/yellow]")
        return

    table = Table(title=f"Starter Kits ({len(catalog.starter_kits)} available)")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="white")
    table.add_column("Audience", style="green")
    table.add_column("Prompts", style="yellow", justify="right")
    table.add_column("Instructions", style="yellow", justify="right")

    for kit in sorted(catalog.starter_kits.values(), key=lambda k: k.id):
        table.add_row(
            kit.id,
            kit.name,
            kit.target_audience,
            str(len(kit.prompts)),
            str(len(kit.instructions)),
        )

    console.print(table)


@kit_group.command("show")
@click.argument("kit_id")
def kit_show(kit_id):
    """Show details and contents of a starter kit."""
    catalog = _load_catalog()

    kit = catalog.starter_kits.get(kit_id)
    if not kit:
        # Try case-insensitive
        for k in catalog.starter_kits.values():
            if k.id.lower() == kit_id.lower():
                kit = k
                break

    if not kit:
        console.print(f"[red]Starter kit not found: {kit_id}[/red]")
        console.print("[dim]Run 'prompt-catalog kit list' to see available kits.[/dim]")
        sys.exit(1)

    console.print(Panel(f"[bold]{kit.name}[/bold]", subtitle=kit.id, border_style="magenta"))
    console.print(f"[dim]Audience:[/dim] {kit.target_audience}")
    console.print(f"[dim]Tags:[/dim] {', '.join(kit.tags)}")
    console.print()
    console.print(kit.description)
    console.print()

    # Prompts in this kit
    console.print("[bold]Prompts included:[/bold]")
    for pid in kit.prompts:
        p = catalog.prompts.get(pid)
        if p:
            console.print(f"  [cyan]{p.id}[/cyan] — {p.title}")
        else:
            console.print(f"  [dim]{pid}[/dim] (not found in catalog)")
    console.print()

    # Instructions in this kit
    console.print("[bold]Instructions loaded:[/bold]")
    for iid in kit.instructions:
        inst = catalog.instructions.get(iid)
        if inst:
            console.print(f"  [green]{inst.stem}[/green] — {inst.name}")
        else:
            console.print(f"  [dim]{iid}[/dim] (not found in catalog)")


@kit_group.command("export")
@click.argument("kit_id")
@click.option("--output", "-o", default=".", help="Output directory")
def kit_export(kit_id, output):
    """Export a starter kit's prompts and instructions to a directory."""
    catalog = _load_catalog()

    kit = catalog.starter_kits.get(kit_id)
    if not kit:
        for k in catalog.starter_kits.values():
            if k.id.lower() == kit_id.lower():
                kit = k
                break

    if not kit:
        console.print(f"[red]Starter kit not found: {kit_id}[/red]")
        sys.exit(1)

    out_dir = Path(output).resolve() / kit.id
    out_dir.mkdir(parents=True, exist_ok=True)

    # Export prompts
    prompts_dir = out_dir / "prompts"
    prompts_dir.mkdir(exist_ok=True)
    count = 0
    for pid in kit.prompts:
        p = catalog.prompts.get(pid)
        if p:
            dest = prompts_dir / p.file_path.name
            dest.write_text(p.file_path.read_text(encoding="utf-8"), encoding="utf-8")
            count += 1

    # Export instructions
    inst_dir = out_dir / "instructions"
    inst_dir.mkdir(exist_ok=True)
    inst_count = 0
    for iid in kit.instructions:
        inst = catalog.instructions.get(iid)
        if inst:
            dest = inst_dir / inst.file_path.name
            dest.write_text(inst.file_path.read_text(encoding="utf-8"), encoding="utf-8")
            inst_count += 1

    console.print(
        f"[green]✓[/green] Exported [cyan]{kit.name}[/cyan] to {out_dir}\n"
        f"  {count} prompts, {inst_count} instruction files"
    )


# ── start (interactive) ─────────────────────────────────────────────


@main.command("start")
def interactive_start():
    """Interactive guided mode — answer questions, get the right prompts."""
    catalog = _load_catalog()

    console.print(
        Panel(
            "[bold]Welcome to Prompt Catalog[/bold]\n\n"
            "Answer a few questions and I'll recommend the right prompts,\n"
            "instructions, and starter kit for your project.",
            border_style="blue",
        )
    )

    # 1. What are you building?
    console.print("\n[bold]What are you building?[/bold]")
    project_types = [
        ("1", "Web application (SaaS, portal, dashboard)"),
        ("2", "Mobile app (Android, iOS, or cross-platform)"),
        ("3", "API / Backend service"),
        ("4", "Desktop application"),
        ("5", "Cloud-native / microservices system"),
        ("6", "Domain-specific application (FinTech, Healthcare, Legal, etc.)"),
    ]
    for num, desc in project_types:
        console.print(f"  [cyan]{num}[/cyan]. {desc}")
    project_choice = RichPrompt.ask("\nSelect", choices=[str(i) for i in range(1, 7)], default="1")

    # 2. Target platform
    console.print("\n[bold]Target platform(s)?[/bold]")
    platform_options = [
        ("1", "Web (browser-based)"),
        ("2", "Windows"),
        ("3", "Linux"),
        ("4", "Android"),
        ("5", "iOS"),
        ("6", "Cloud (multi-platform)"),
    ]
    for num, desc in platform_options:
        console.print(f"  [cyan]{num}[/cyan]. {desc}")
    plat_choice = RichPrompt.ask("\nSelect", choices=[str(i) for i in range(1, 7)], default="1")
    platform_map = {"1": "web", "2": "windows", "3": "linux", "4": "android", "5": "ios", "6": "cloud"}
    selected_platform = platform_map[plat_choice]

    # 3. Experience level
    console.print("\n[bold]Your experience level?[/bold]")
    for i, level in enumerate(SKILL_ORDER, 1):
        console.print(f"  [cyan]{i}[/cyan]. {level.capitalize()}")
    skill_choice = RichPrompt.ask("\nSelect", choices=["1", "2", "3", "4"], default="2")
    selected_skill = SKILL_ORDER[int(skill_choice) - 1]

    # 4. Domain (if applicable)
    selected_domain = None
    if project_choice == "6":
        console.print("\n[bold]Which domain?[/bold]")
        domain_prompts = catalog.filter_prompts(category="domains")
        domain_map = {}
        for i, dp in enumerate(sorted(domain_prompts, key=lambda x: x.title), 1):
            console.print(f"  [cyan]{i}[/cyan]. {dp.title}")
            domain_map[str(i)] = dp
        if domain_map:
            dom_choice = RichPrompt.ask(
                "\nSelect",
                choices=[str(i) for i in range(1, len(domain_map) + 1)],
                default="1",
            )
            selected_domain = domain_map[dom_choice]

    # Build recommendations
    console.print("\n" + "─" * 60)
    console.print("[bold green]Recommended Prompt Stack[/bold green]\n")

    recommended: list[str] = []

    # Always include requirements
    recommended.append("PLAN-REQ-001")

    # Project type mapping
    if project_choice == "1":  # Web app
        recommended.extend(["PLAN-REQ-003", "ARCH-SYS-001", "DEV-WEB-001", "DEV-API-001"])
    elif project_choice == "2":  # Mobile
        recommended.extend(["PLAN-REQ-003", "ARCH-SYS-001", "DEV-MOB-001", "DEV-API-001"])
    elif project_choice == "3":  # API
        recommended.extend(["PLAN-REQ-002", "ARCH-SYS-001", "DEV-API-001"])
    elif project_choice == "4":  # Desktop
        recommended.extend(["PLAN-REQ-003", "ARCH-SYS-001", "DEV-DESK-001"])
    elif project_choice == "5":  # Cloud-native
        recommended.extend([
            "PLAN-REQ-002", "ARCH-CLOUD-001", "ARCH-MICRO-001",
            "ARCH-DATA-001", "DEV-API-001", "DEPLOY-IAC-001",
        ])

    # Always include security and testing
    recommended.extend(["SEC-THREAT-001", "TEST-UNIT-001", "DEPLOY-CICD-001", "OPS-MON-001"])

    # Add domain prompt
    if selected_domain:
        recommended.insert(4, selected_domain.id)

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for r in recommended:
        if r not in seen:
            seen.add(r)
            unique.append(r)
    recommended = unique

    # Display
    console.print("[bold]Prompts:[/bold]")
    for i, pid in enumerate(recommended, 1):
        p = catalog.prompts.get(pid)
        if p:
            skill_ok = SKILL_ORDER.index(p.skill_level) <= SKILL_ORDER.index(selected_skill)
            icon = "[green]✓[/green]" if skill_ok else "[yellow]⚠[/yellow]"
            console.print(f"  {icon} {i}. [cyan]{p.id}[/cyan] — {p.title} [{p.skill_level}]")
        else:
            console.print(f"  [dim]  {i}. {pid} (not in catalog)[/dim]")

    # Recommend instructions
    console.print("\n[bold]Instructions to load:[/bold]")
    inst_list = [
        ("accuracy.instructions", "Always — anti-hallucination guardrails"),
        ("security.instructions", "Always — security baseline"),
        ("adversarial-evaluation.instructions", "Always — adversarial testing"),
    ]

    platform_inst = f"{selected_platform}.instructions"
    inst_list.append((platform_inst, f"Platform — {selected_platform} guidance"))

    console.print()
    for stem, reason in inst_list:
        inst = catalog.instructions.get(stem)
        if inst:
            console.print(f"  [green]✓[/green] [green]{stem}[/green] — {reason}")
        else:
            console.print(f"  [dim]  {stem} — {reason}[/dim]")

    # Check for matching starter kit
    console.print("\n[bold]Matching starter kit:[/bold]")
    matched_kit = None
    for kit in catalog.starter_kits.values():
        kit_tags = set(kit.tags)
        if selected_platform in kit_tags or (selected_domain and selected_domain.subcategory in kit_tags):
            matched_kit = kit
            break

    if matched_kit:
        console.print(f"  [magenta]→[/magenta] [cyan]{matched_kit.id}[/cyan] — {matched_kit.name}")
        console.print(f"    Run: [cyan]prompt-catalog kit show {matched_kit.id}[/cyan]")
    else:
        console.print("  [dim]No exact kit match — use the prompts listed above.[/dim]")

    console.print(
        "\n[dim]Tip: Run [cyan]prompt-catalog show PROMPT-ID[/cyan] to see full prompt details.[/dim]"
    )


# ── validate ─────────────────────────────────────────────────────────


@main.command("validate")
@click.option("--prompts", "check_prompts", is_flag=True, help="Validate prompt YAML files only")
@click.option("--instructions", "check_instructions", is_flag=True, help="Validate instruction files only")
@click.option("--index", "check_index", is_flag=True, help="Validate index.json only")
@click.option("--kits", "check_kits", is_flag=True, help="Validate starter kit references only")
@click.option("--json-output", "json_out", is_flag=True, help="Output results as JSON")
def validate(check_prompts, check_instructions, check_index, check_kits, json_out):
    """Validate prompts, instructions, index, and starter kits."""
    from .validator import validate_all, validate_prompts as vp, validate_instructions as vi
    from .validator import validate_index as vidx, validate_kits as vk

    root = _find_catalog_root()

    # If no specific flag, validate everything
    run_all = not (check_prompts or check_instructions or check_index or check_kits)

    if run_all:
        results = validate_all(root)
    else:
        results = {}
        if check_prompts:
            results["prompts"] = vp(root)
        if check_instructions:
            results["instructions"] = vi(root)
        if check_index:
            results["index"] = vidx(root)
        if check_kits:
            results["starter-kits"] = vk(root)

    total_errors = sum(r.error_count for r in results.values())
    total_warnings = sum(r.warning_count for r in results.values())
    total_checked = sum(r.files_checked for r in results.values())
    total_passed = sum(r.files_passed for r in results.values())

    if json_out:
        import json as jsonlib
        out = {
            "summary": {
                "files_checked": total_checked,
                "files_passed": total_passed,
                "errors": total_errors,
                "warnings": total_warnings,
            },
            "categories": {
                cat: {
                    "files_checked": r.files_checked,
                    "files_passed": r.files_passed,
                    "issues": [
                        {"file": i.file, "message": i.message, "severity": i.severity}
                        for i in r.issues
                    ],
                }
                for cat, r in results.items()
            },
        }
        click.echo(jsonlib.dumps(out, indent=2))
    else:
        console.print(Panel("[bold]Prompt Catalog Validation[/bold]", border_style="blue"))

        for cat, r in results.items():
            if r.ok and not r.issues:
                console.print(
                    f"\n[bold]{cat}[/bold]: "
                    f"[green]✓ {r.files_passed}/{r.files_checked} files passed[/green]"
                )
            else:
                console.print(
                    f"\n[bold]{cat}[/bold]: "
                    f"[{'red' if r.error_count else 'yellow'}]"
                    f"{r.files_passed}/{r.files_checked} passed, "
                    f"{r.error_count} error(s), {r.warning_count} warning(s)"
                    f"[/{'red' if r.error_count else 'yellow'}]"
                )
                for issue in r.issues:
                    color = "red" if issue.severity == "error" else "yellow"
                    icon = "✗" if issue.severity == "error" else "⚠"
                    console.print(f"  [{color}]{icon}[/{color}] {issue.file}: {issue.message}")

        console.print()
        if total_errors == 0:
            console.print(
                f"[bold green]✓ All checks passed[/bold green] "
                f"({total_checked} files, {total_warnings} warnings)"
            )
        else:
            console.print(
                f"[bold red]✗ Validation failed[/bold red] "
                f"({total_errors} errors, {total_warnings} warnings in {total_checked} files)"
            )

    sys.exit(1 if total_errors > 0 else 0)


# ── serve ────────────────────────────────────────────────────────────


@main.command("serve")
def serve():
    """Start the MCP server (stdio transport)."""
    os.environ.setdefault("CATALOG_ROOT", str(_find_catalog_root()))
    from .server import main as server_main

    server_main()


if __name__ == "__main__":
    main()

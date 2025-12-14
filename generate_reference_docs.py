#!/usr/bin/env python3

from __future__ import annotations

import ast
import inspect
import os
import sys
from pathlib import Path
from typing import Any


DOCS_ROOT = Path(__file__).resolve().parent
GENERATED_DIR = DOCS_ROOT / "docs" / "_generated"


def _find_fast_agent_repo() -> Path:
    """
    Locate a local fast-agent repo checkout.

    Uses FAST_AGENT_REPO_PATH when set, otherwise assumes ../fast-agent next to this repo.
    """
    repo_override = os.getenv("FAST_AGENT_REPO_PATH")
    candidate = Path(repo_override).resolve() if repo_override else (DOCS_ROOT.parent / "fast-agent")
    candidate = candidate.resolve()

    expected = candidate / "src" / "fast_agent" / "llm" / "model_factory.py"
    if expected.exists():
        return candidate

    raise SystemExit(
        "Could not locate fast-agent source.\n"
        "Set FAST_AGENT_REPO_PATH to the fast-agent repo root (the directory containing `src/fast_agent`)."
    )


def _try_enable_fast_agent_import(repo_root: Path) -> None:
    """
    Best-effort enable imports from a local `fast-agent` checkout.

    Some generated references (e.g. RequestParams field docs) require importing fast_agent,
    which may fail if the docs environment doesn't have runtime deps installed.
    """
    src_root = repo_root / "src"
    if src_root.exists():
        sys.path.insert(0, str(src_root))
    sys.path.insert(0, str(repo_root))


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _md_code(lang: str, code: str) -> str:
    return f"```{lang}\n{code.rstrip()}\n```\n"


def _format_signature(name: str, func: Any) -> str:
    sig = str(inspect.signature(func))
    return f"{name}{sig}"


def generate_workflows_reference() -> str:
    from fast_agent.core.fastagent import FastAgent

    fast = FastAgent("docs-reference")

    workflows: list[tuple[str, Any]] = [
        ("chain", fast.chain),
        ("parallel", fast.parallel),
        ("evaluator_optimizer", fast.evaluator_optimizer),
        ("router", fast.router),
        ("orchestrator", fast.orchestrator),
        ("iterative_planner", fast.iterative_planner),
        ("maker", fast.maker),
    ]

    lines: list[str] = []
    lines.append("<!--\n")
    lines.append("  GENERATED FILE — DO NOT EDIT.\n")
    lines.append("  Source: generate_reference_docs.py\n")
    lines.append("-->\n\n")
    lines.append("## Workflow Decorators (Generated)\n\n")
    lines.append(
        "These signatures are generated from the installed `fast_agent` package to prevent drift.\n\n"
    )

    for name, method in workflows:
        lines.append(f"### `{name}`\n\n")
        lines.append(_md_code("python", _format_signature(f"fast.{name}", method)))

    return "".join(lines)


def generate_request_params_reference() -> str:
    from fast_agent.types import RequestParams

    lines: list[str] = []
    lines.append("<!--\n")
    lines.append("  GENERATED FILE — DO NOT EDIT.\n")
    lines.append("  Source: generate_reference_docs.py\n")
    lines.append("-->\n\n")
    lines.append("### Available `RequestParams` Fields (Generated)\n\n")
    lines.append("| Field | Type | Default | Description |\n")
    lines.append("| --- | --- | --- | --- |\n")

    for field_name, field_info in RequestParams.model_fields.items():
        annotation = field_info.annotation
        type_str = getattr(annotation, "__name__", None) or str(annotation)
        default = field_info.default
        if default is None and field_info.default_factory is not None:
            default_str = "`<factory>`"
        else:
            default_str = "`None`" if default is None else f"`{default!r}`"

        desc = (field_info.description or "").replace("\n", " ").strip()
        lines.append(f"| `{field_name}` | `{type_str}` | {default_str} | {desc} |\n")

    return "".join(lines)


def _format_alias_table(entries: list[tuple[str, str]], *, two_column: bool) -> str:
    def fmt_cell(s: str) -> str:
        return f"`{s}`" if s else ""

    entries = sorted(entries, key=lambda t: t[0].lower())

    if not entries:
        return "_No aliases defined._\n"

    if two_column:
        lines: list[str] = []
        lines.append("| Model Alias | Maps to |\n")
        lines.append("| --- | --- |\n")
        for alias, target in entries:
            lines.append(f"| {fmt_cell(alias)} | {fmt_cell(target)} |\n")
        return "".join(lines)

    # 4-column layout (two alias columns side-by-side)
    half = (len(entries) + 1) // 2
    left = entries[:half]
    right = entries[half:]

    lines = []
    lines.append("| Model Alias | Maps to | Model Alias | Maps to |\n")
    lines.append("| --- | --- | --- | --- |\n")
    for i in range(half):
        a1, t1 = left[i]
        if i < len(right):
            a2, t2 = right[i]
        else:
            a2, t2 = "", ""
        lines.append(f"| {fmt_cell(a1)} | {fmt_cell(t1)} | {fmt_cell(a2)} | {fmt_cell(t2)} |\n")
    return "".join(lines)


def _provider_name_map(repo_root: Path) -> dict[str, str]:
    """
    Map Provider enum member name -> provider config string (e.g. OPENAI -> "openai").
    """
    provider_types = repo_root / "src" / "fast_agent" / "llm" / "provider_types.py"
    tree = ast.parse(provider_types.read_text(encoding="utf-8"))

    mapping: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "Provider":
            for stmt in node.body:
                if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(
                    stmt.targets[0], ast.Name
                ):
                    key = stmt.targets[0].id
                    # Provider members are assigned tuples like ("openai", "OpenAI")
                    if isinstance(stmt.value, ast.Tuple) and stmt.value.elts:
                        first = stmt.value.elts[0]
                        if isinstance(first, ast.Constant) and isinstance(first.value, str):
                            mapping[key] = first.value
    return mapping


def _load_model_factory_constants(
    repo_root: Path,
) -> tuple[dict[str, str], dict[str, str], set[str], set[str]]:
    """
    Load ModelFactory.MODEL_ALIASES and ModelFactory.DEFAULT_PROVIDERS from source using AST.
    Returns (model_aliases, default_providers, effort_suffixes).
    """
    model_factory = repo_root / "src" / "fast_agent" / "llm" / "model_factory.py"
    tree = ast.parse(model_factory.read_text(encoding="utf-8"))

    provider_map = _provider_name_map(repo_root)
    provider_names: set[str] = set(provider_map.values())

    model_aliases: dict[str, str] = {}
    default_providers: dict[str, str] = {}
    effort_suffixes: set[str] = set()

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "ModelFactory":
            for stmt in node.body:
                if not isinstance(stmt, ast.Assign) or len(stmt.targets) != 1:
                    continue
                if not isinstance(stmt.targets[0], ast.Name):
                    continue
                target_name = stmt.targets[0].id

                if target_name == "MODEL_ALIASES" and isinstance(stmt.value, ast.Dict):
                    for k, v in zip(stmt.value.keys, stmt.value.values):
                        if (
                            isinstance(k, ast.Constant)
                            and isinstance(k.value, str)
                            and isinstance(v, ast.Constant)
                            and isinstance(v.value, str)
                        ):
                            model_aliases[k.value] = v.value

                if target_name == "DEFAULT_PROVIDERS" and isinstance(stmt.value, ast.Dict):
                    for k, v in zip(stmt.value.keys, stmt.value.values):
                        if not (isinstance(k, ast.Constant) and isinstance(k.value, str)):
                            continue
                        # Values are Provider.OPENAI etc
                        if (
                            isinstance(v, ast.Attribute)
                            and isinstance(v.value, ast.Name)
                            and v.value.id == "Provider"
                        ):
                            provider_member = v.attr
                            provider_name = provider_map.get(provider_member)
                            if provider_name:
                                default_providers[k.value] = provider_name

                if target_name == "EFFORT_MAP" and isinstance(stmt.value, ast.Dict):
                    for k in stmt.value.keys:
                        if isinstance(k, ast.Constant) and isinstance(k.value, str):
                            effort_suffixes.add(k.value.lower())

    return model_aliases, default_providers, effort_suffixes, provider_names


def _infer_provider_for_model_string(
    model_string: str, *, default_providers: dict[str, str], provider_names: set[str], effort_suffixes: set[str]
) -> str | None:
    """
    Infer provider from a model string using the same high-level rules as ModelFactory.parse_model_string.
    """
    base = model_string.rsplit(":", 1)[0]
    parts = base.split(".")

    # Strip reasoning suffix if present
    if len(parts) > 1 and parts[-1].lower() in effort_suffixes:
        base = ".".join(parts[:-1])
        parts = base.split(".")

    if parts and parts[0] in provider_names:
        return parts[0]

    return default_providers.get(base)


def _include_default_model_name(provider_name: str, model_name: str) -> bool:
    """
    Heuristic for which "default provider" model names to show in provider docs.

    Goal: keep tables readable by excluding heavily versioned names.
    """
    # Exclude date/version stamped releases in the alias tables
    if "-20" in model_name:
        return False
    # Exclude long Bedrock ids etc (not shown via this table)
    if provider_name == "bedrock":
        return False
    return True


def generate_model_alias_table(
    provider_name: str,
    *,
    include_default_models: bool,
    two_column: bool = True,
    repo_root: Path,
) -> str:
    """
    Generate a provider-specific model alias table from fast-agent source-of-truth.

    Includes:
      - "default provider" model names (e.g. `gpt-5` defaults to OpenAI)
      - short aliases from ModelFactory.MODEL_ALIASES (e.g. `sonnet` -> `claude-sonnet-4-5`)
    """
    model_aliases, default_providers, effort_suffixes, provider_names = _load_model_factory_constants(
        repo_root
    )

    entries: dict[str, str] = {}

    if include_default_models:
        for model_name, default_provider in default_providers.items():
            if default_provider == provider_name and _include_default_model_name(provider_name, model_name):
                entries[model_name] = model_name

    for alias, target in model_aliases.items():
        inferred = _infer_provider_for_model_string(
            target,
            default_providers=default_providers,
            provider_names=provider_names,
            effort_suffixes=effort_suffixes,
        )
        if inferred == provider_name:
            entries[alias] = target

    return _format_alias_table(list(entries.items()), two_column=two_column)


def main() -> int:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    repo_root = _find_fast_agent_repo()

    # Alias tables are generated from source (AST) so they work even when fast_agent runtime deps
    # aren't installed in the docs environment.
    _write(
        GENERATED_DIR / "model_aliases_anthropic.md",
        generate_model_alias_table(
            "anthropic",
            include_default_models=False,
            two_column=False,
            repo_root=repo_root,
        ),
    )
    _write(
        GENERATED_DIR / "model_aliases_openai.md",
        generate_model_alias_table(
            "openai",
            include_default_models=True,
            two_column=False,
            repo_root=repo_root,
        ),
    )
    _write(
        GENERATED_DIR / "model_aliases_groq.md",
        generate_model_alias_table(
            "groq",
            include_default_models=False,
            two_column=True,
            repo_root=repo_root,
        ),
    )
    _write(
        GENERATED_DIR / "model_aliases_deepseek.md",
        generate_model_alias_table(
            "deepseek",
            include_default_models=False,
            two_column=True,
            repo_root=repo_root,
        ),
    )
    _write(
        GENERATED_DIR / "model_aliases_google.md",
        generate_model_alias_table(
            "google",
            include_default_models=False,
            two_column=True,
            repo_root=repo_root,
        ),
    )
    _write(
        GENERATED_DIR / "model_aliases_xai.md",
        generate_model_alias_table(
            "xai",
            include_default_models=True,
            two_column=True,
            repo_root=repo_root,
        ),
    )

    # Best-effort: these require importing `fast_agent` (and its runtime deps).
    _try_enable_fast_agent_import(repo_root)
    try:
        _write(GENERATED_DIR / "workflows_reference.md", generate_workflows_reference())
        _write(GENERATED_DIR / "request_params_reference.md", generate_request_params_reference())
    except Exception as exc:
        _write(
            GENERATED_DIR / "_generation_warnings.md",
            f"Generated alias tables successfully, but skipped import-based references: `{type(exc).__name__}: {exc}`\n",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

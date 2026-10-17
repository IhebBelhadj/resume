"""The one place that talks to a model: the local Claude Code CLI in headless mode.

Runs `claude -p` on the user's logged-in subscription (no API key), with our own system
prompt and no tools unless a call asks for some (the cover letter uses web search), and
returns the JSON that `--json-schema` forces. To move to the Anthropic API
later, reimplement `complete_json` here; nothing else needs to change.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent / "prompts"
DEFAULT_MODEL = os.environ.get("RESUME_MODEL", "opus")
TIMEOUT_S = 900


class LLMError(RuntimeError):
    pass


def prompt(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")


def complete_json(user: str, schema: dict, system: str, model: str | None = None,
                  tools: list[str] | None = None) -> tuple[dict, dict]:
    """Send one prompt, return (structured output, run info: model/cost/duration)."""
    exe = shutil.which("claude")
    if not exe:
        raise LLMError("the `claude` CLI is not on PATH (install Claude Code and log in)")
    cmd = [
        exe, "-p",
        "--output-format", "json",
        "--json-schema", json.dumps(schema),
        "--system-prompt", system,
        "--tools", ",".join(tools or []),
        *(["--allowedTools", ",".join(tools)] if tools else []),
        "--no-session-persistence",
        "--model", model or DEFAULT_MODEL,
    ]
    try:
        proc = subprocess.run(cmd, input=user, capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        raise LLMError(f"claude -p timed out after {TIMEOUT_S}s") from None
    try:
        out = json.loads(proc.stdout)
    except json.JSONDecodeError:
        detail = (proc.stderr or proc.stdout).strip()[-1500:]
        raise LLMError(f"claude -p failed (exit {proc.returncode}); logged in? Run `claude` then /login.\n{detail}") from None
    if out.get("is_error") or out.get("structured_output") is None:
        raise LLMError(f"claude -p returned no result ({out.get('subtype')}): {str(out.get('result'))[:1500]}")
    info = {
        "model": next(iter(out.get("modelUsage") or {}), model or DEFAULT_MODEL),
        "cost_usd": out.get("total_cost_usd"),
        "seconds": round((out.get("duration_ms") or 0) / 1000, 1),
    }
    return out["structured_output"], info

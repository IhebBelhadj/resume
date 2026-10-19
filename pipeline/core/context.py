"""Load and index the context/ knowledge base.

Experiences, projects and studies are Markdown files: YAML frontmatter holds the structured
metadata the renderer and validator need; the body is the raw fact dump that resume bullets
are generated from.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONTEXT_DIR = ROOT / "context"


class ContextError(ValueError):
    pass


@dataclass
class Context:
    profile: dict
    skills: list[dict]
    experiences: dict[str, dict] = field(default_factory=dict)
    projects: dict[str, dict] = field(default_factory=dict)
    studies: dict[str, dict] = field(default_factory=dict)

    @property
    def all_skills(self) -> set[str]:
        return {item for cat in self.skills for item in cat["items"]}


def _load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ContextError(f"{path}: expected a mapping at top level")
    return data


def _load_md(path: Path) -> dict:
    """Split `---\\n<yaml>\\n---\\n<body>` into the frontmatter dict plus `raw` (the body)."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ContextError(f"{path}: must start with a '---' YAML frontmatter block")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ContextError(f"{path}: unterminated frontmatter (missing closing '---')")
    data = yaml.safe_load(text[4:end]) or {}
    if not isinstance(data, dict):
        raise ContextError(f"{path}: frontmatter must be a mapping")
    if "raw" in data:
        raise ContextError(f"{path}: 'raw' is reserved for the body")
    data["raw"] = text[end + 5:].strip()
    return data


def _load_dir(sub: str, required: tuple[str, ...]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for path in sorted((CONTEXT_DIR / sub).glob("*.md")):
        item = _load_md(path)
        missing = [k for k in required if k not in item]
        if missing:
            raise ContextError(f"{path}: missing keys {missing}")
        if item["id"] != path.stem:
            raise ContextError(f"{path}: id {item['id']!r} must match filename")
        if item["id"] in out:
            raise ContextError(f"{path}: duplicate id {item['id']!r}")
        item["_path"] = str(path.relative_to(ROOT))
        out[item["id"]] = item
    return out


def load_context() -> Context:
    profile = _load_yaml(CONTEXT_DIR / "profile.yaml")
    skills = _load_yaml(CONTEXT_DIR / "skills.yaml")["categories"]
    ctx = Context(profile=profile, skills=skills)
    ctx.experiences = _load_dir("experiences", ("id", "company", "titles", "location", "start", "dates"))
    ctx.projects = _load_dir("projects", ("id", "name"))
    ctx.studies = _load_dir("studies", ("id", "school", "degrees", "start", "dates"))
    return ctx


def dump_context(ctx: Context) -> str:
    """Every skill and context file (frontmatter + raw body) in one document."""
    out: list[str] = ["# SKILLS (category id (label): items)"]
    for c in ctx.skills:
        out.append(f"- {c['id']} ({c['label']}): {', '.join(c['items'])}")

    def dump_items(title: str, items: dict, head) -> None:
        out.append(f"\n# {title}")
        for it in sorted(items.values(), key=lambda x: str(x.get("start", "")), reverse=True):
            out.append(f"\n## {it['id']}: {head(it)}")
            if it.get("stack"):
                out.append(f"stack: {', '.join(it['stack'])}")
            raw = re.sub(r"<!--.*?-->", "", it["raw"], flags=re.S).strip()
            if raw:
                out.append(re.sub(r"(?m)^#", "###", raw))

    dump_items("EXPERIENCES", ctx.experiences,
               lambda e: f"{e['company']}, {e['location']} ({e['dates']}); titles: {e['titles']}")
    dump_items("PROJECTS", ctx.projects, lambda p: f"{p['name']} <{p.get('url', '')}>")
    dump_items("STUDIES", ctx.studies, lambda s: f"{s['school']} ({s['dates']}); degrees: {s['degrees']}")
    if ctx.profile.get("languages"):
        out.append("\n# LANGUAGES (printed by code)\n" + ", ".join(l["en"] for l in ctx.profile["languages"]))
    if ctx.profile.get("notes"):
        out.append("\n# PROFILE NOTES\n" + ctx.profile["notes"].strip())
    return "\n".join(out)

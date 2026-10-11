"""Load and index the context/ knowledge base."""

from __future__ import annotations

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
    # bullet id -> (owner id, bullet dict), across experiences/projects/studies
    bullets: dict[str, tuple[str, dict]] = field(default_factory=dict)
    summaries: dict[str, dict] = field(default_factory=dict)

    @property
    def all_skills(self) -> set[str]:
        return {item for cat in self.skills for item in cat["items"]}


def _load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ContextError(f"{path}: expected a mapping at top level")
    return data


def _load_dir(ctx: Context, sub: str, required: tuple[str, ...]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for path in sorted((CONTEXT_DIR / sub).glob("*.yaml")):
        item = _load_yaml(path)
        missing = [k for k in required if k not in item]
        if missing:
            raise ContextError(f"{path}: missing keys {missing}")
        if item["id"] != path.stem:
            raise ContextError(f"{path}: id {item['id']!r} must match filename")
        if item["id"] in out:
            raise ContextError(f"{path}: duplicate id {item['id']!r}")
        for b in item.get("bullets") or []:
            if b["id"] in ctx.bullets:
                raise ContextError(f"{path}: duplicate bullet id {b['id']!r}")
            ctx.bullets[b["id"]] = (item["id"], b)
        item["_path"] = str(path.relative_to(ROOT))
        out[item["id"]] = item
    return out


def load_context() -> Context:
    profile = _load_yaml(CONTEXT_DIR / "profile.yaml")
    skills = _load_yaml(CONTEXT_DIR / "skills.yaml")["categories"]
    ctx = Context(profile=profile, skills=skills)
    ctx.summaries = {s["id"]: s for s in profile.get("summaries", [])}
    ctx.experiences = _load_dir(ctx, "experiences", ("id", "company", "titles", "location", "start", "dates"))
    ctx.projects = _load_dir(ctx, "projects", ("id", "name"))
    ctx.studies = _load_dir(ctx, "studies", ("id", "school", "degrees", "start", "dates"))

    for bid, (owner, b) in ctx.bullets.items():
        v = b.get("variant_of")
        if v and (v not in ctx.bullets or ctx.bullets[v][0] != owner):
            raise ContextError(f"bullet {bid!r}: variant_of {v!r} not found in {owner!r}")
    return ctx

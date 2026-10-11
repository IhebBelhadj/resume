"""Validate a selection.yaml against the context and resolve it into a render model.

A selection only *references* context by id. The only free text it may carry is
`summary.text` and per-bullet `text` rewrites, which are reported back so a human
can review them (they must not introduce facts that are not in context/).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .context import Context

DEFAULT_SECTIONS = ["summary", "skills", "experience", "projects", "education"]


class SelectionError(ValueError):
    def __init__(self, errors: list[str]):
        super().__init__("\n".join(errors))
        self.errors = errors


@dataclass
class Resolved:
    model: dict
    warnings: list[str] = field(default_factory=list)
    rewrites: list[tuple[str, str, str]] = field(default_factory=list)  # (id, original, new)


def load_selection(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _ref(entry) -> tuple[str, str | None]:
    """A list entry is either `id` or `{id, text}`."""
    if isinstance(entry, str):
        return entry, None
    return entry["id"], entry.get("text")


def _stack(spec, item: dict, ctx: Context, where: str, errors: list[str]) -> list[str]:
    if spec is False or spec is None and not item.get("stack"):
        return []
    if spec is None or spec is True:
        return list(item.get("stack") or [])
    allowed = set(item.get("stack") or []) | ctx.all_skills
    for s in spec:
        if s not in allowed:
            errors.append(f"{where}: stack item {s!r} not in its context stack or skills.yaml")
    return list(spec)


def resolve(sel: dict, ctx: Context) -> Resolved:
    errors: list[str] = []
    res = Resolved(model={})
    used_bullets: set[str] = set()

    def bullets_for(owner_id: str, refs, where: str) -> list[str]:
        out = []
        chosen_roots: dict[str, str] = {}
        for entry in refs or []:
            bid, text = _ref(entry)
            if bid not in ctx.bullets:
                errors.append(f"{where}: unknown bullet {bid!r}")
                continue
            owner, b = ctx.bullets[bid]
            if owner != owner_id:
                errors.append(f"{where}: bullet {bid!r} belongs to {owner!r}")
                continue
            if bid in used_bullets:
                errors.append(f"{where}: bullet {bid!r} used twice")
            used_bullets.add(bid)
            root = b.get("variant_of") or bid
            if root in chosen_roots:
                res.warnings.append(f"{where}: {bid!r} and {chosen_roots[root]!r} are variants of the same bullet")
            chosen_roots[root] = bid
            if text and text.strip() != b["text"].strip():
                res.rewrites.append((bid, b["text"], text))
            out.append(text or b["text"])
        return out

    # summary
    summ = sel.get("summary")
    summary_text = None
    if isinstance(summ, str):
        if summ not in ctx.summaries:
            errors.append(f"summary: unknown summary id {summ!r}")
        else:
            summary_text = ctx.summaries[summ]["text"]
    elif isinstance(summ, dict):
        base = summ.get("id")
        if base and base not in ctx.summaries:
            errors.append(f"summary: unknown summary id {base!r}")
        summary_text = summ.get("text") or (ctx.summaries[base]["text"] if base in ctx.summaries else None)
        if summ.get("text"):
            res.rewrites.append((base or "summary", ctx.summaries.get(base, {}).get("text", ""), summ["text"]))

    # skills
    cats = {c["id"]: c for c in ctx.skills}
    skills = []
    for i, spec in enumerate(sel.get("skills") or []):
        cat = cats.get(spec.get("category"))
        label = spec.get("label") or (cat["label"] if cat else None)
        if not label:
            errors.append(f"skills[{i}]: unknown category {spec.get('category')!r} and no label")
            continue
        items = spec.get("items") if spec.get("items") is not None else (cat["items"] if cat else [])
        for it in items:
            if it not in ctx.all_skills:
                errors.append(f"skills[{i}] ({label}): {it!r} not in skills.yaml")
        skills.append({"label": label, "items": list(items)})

    # experiences
    experiences = []
    for spec in sel.get("experiences") or []:
        eid = spec["id"] if isinstance(spec, dict) else spec
        spec = spec if isinstance(spec, dict) else {}
        e = ctx.experiences.get(eid)
        if not e:
            errors.append(f"experiences: unknown id {eid!r}")
            continue
        title = spec.get("title") or e["titles"][0]
        if title not in e["titles"]:
            errors.append(f"experiences.{eid}: title {title!r} not in {e['titles']}")
        refs = spec.get("bullets")
        if refs is None:  # default: all non-variant bullets
            refs = [b["id"] for b in e.get("bullets") or [] if not b.get("variant_of")]
        experiences.append({
            "id": eid,
            "start": str(e["start"]),
            "title": title,
            "company": e["company"],
            "location": e["location"],
            "dates": e["dates"],
            "bullets": bullets_for(eid, refs, f"experiences.{eid}"),
            "stack": _stack(spec.get("stack"), e, ctx, f"experiences.{eid}", errors),
        })
    experiences.sort(key=lambda x: x["start"], reverse=True)

    # projects (keep selection order: most relevant first)
    projects = []
    for spec in sel.get("projects") or []:
        pid = spec["id"] if isinstance(spec, dict) else spec
        spec = spec if isinstance(spec, dict) else {}
        p = ctx.projects.get(pid)
        if not p:
            errors.append(f"projects: unknown id {pid!r}")
            continue
        refs = spec.get("bullets")
        if refs is None:
            refs = [b["id"] for b in p.get("bullets") or [] if not b.get("variant_of")][:1]
        projects.append({
            "name": p["name"],
            "url": p.get("url"),
            "bullets": bullets_for(pid, refs, f"projects.{pid}"),
            "stack": _stack(spec.get("stack", False), p, ctx, f"projects.{pid}", errors),
        })

    # education
    education = []
    for spec in sel.get("education") or []:
        sid = spec["id"] if isinstance(spec, dict) else spec
        spec = spec if isinstance(spec, dict) else {}
        s = ctx.studies.get(sid)
        if not s:
            errors.append(f"education: unknown id {sid!r}")
            continue
        degree = spec.get("degree") or s["degrees"][0]
        if degree not in s["degrees"]:
            errors.append(f"education.{sid}: degree {degree!r} not in {s['degrees']}")
        education.append({
            "start": str(s["start"]),
            "degree": degree,
            "school": s["school"],
            "dates": s["dates"],
            "bullets": bullets_for(sid, spec.get("bullets", []), f"education.{sid}"),
        })
    education.sort(key=lambda x: x["start"], reverse=True)

    sections = sel.get("sections") or DEFAULT_SECTIONS
    for s in sections:
        if s not in DEFAULT_SECTIONS:
            errors.append(f"sections: unknown section {s!r}")

    if errors:
        raise SelectionError(errors)

    res.model = {
        "profile": ctx.profile,
        "sections": sections,
        "summary": summary_text,
        "skills": skills,
        "experiences": experiences,
        "projects": projects,
        "education": education,
    }
    return res

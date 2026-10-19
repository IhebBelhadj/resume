"""Write resume.yaml for an offer: one model call picks entries by id and writes the summary and bullets,
then `resume.expand` fills in everything else from context/. If `expand` rejects the selection
(unknown ids/skills, a long experience without bullets), the model gets the errors and one retry.
With `feedback` (the reviewer's notes from `score`), the model revises the previous resume.yaml."""

from __future__ import annotations

from pathlib import Path

from .context import Context, dump_context
from .llm import complete_json, prompt
from .resume import LANGS, ResumeError, expand, long_experiences, write_resume

_STR_LIST = {"type": "array", "items": {"type": "string"}}


def _bullets(n: int) -> dict:
    return {**_STR_LIST, "maxItems": n}


def _obj(**props) -> dict:
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


SCHEMA = _obj(
    offer=_obj(company={"type": "string"}, role={"type": "string"}, url={"type": "string"}, country={"type": "string"}),
    lang={"type": "string", "enum": list(LANGS)},
    summary={"type": "string"},
    skills={"type": "array", "items": _obj(category={"type": "string"}, label={"type": "string"}, items=_STR_LIST)},
    experiences={"type": "array", "items": _obj(id={"type": "string"}, title={"type": "string"}, bullets=_bullets(5), stack=_STR_LIST)},
    projects={"type": "array", "items": _obj(id={"type": "string"}, bullets=_bullets(3), stack=_STR_LIST)},
    education=_STR_LIST,
    gaps=_STR_LIST,
)


def to_selection(out: dict, max_pages: int) -> dict:
    """Model output -> selection by id (drop empty optionals)."""
    return {
        "offer": out["offer"],
        "lang": out["lang"],
        "max_pages": max_pages,
        "summary": out["summary"].strip() or None,
        "skills": [{k: v for k, v in s.items() if k != "label" or v} for s in out["skills"]],
        "experiences": out["experiences"],
        "projects": out["projects"],
        "education": out["education"],
        "gaps": out["gaps"],
    }


def tailor(offer_dir: Path, ctx: Context, model: str | None = None, max_pages: int = 2,
           feedback: str | None = None) -> tuple[dict, dict]:
    """Write offer_dir/resume.yaml; return (resume document, model run info)."""
    offer = (offer_dir / "offer.md").read_text(encoding="utf-8")
    msg = (f"# CONTEXT\n\n{dump_context(ctx)}\n\n# OFFER\n\n{offer}\n\nPage budget: {max_pages} page(s).\n"
           f"Experiences that need at least one bullet if shown: {', '.join(long_experiences(ctx))}.\n")
    if feedback:
        previous = (offer_dir / "resume.yaml").read_text(encoding="utf-8")
        msg += f"\n# PREVIOUS RESUME (resume.yaml)\n\n{previous}\n\n# REVIEWER FEEDBACK\n\n{feedback}\n"
    out, info = complete_json(msg, SCHEMA, prompt("tailor"), model)
    try:
        doc = expand(to_selection(out, max_pages), ctx)
    except ResumeError as e:
        errors = "\n".join(f"- {err}" for err in e.errors)
        msg += f"\n# YOUR PREVIOUS ANSWER WAS REJECTED\n\nFix these and answer again:\n{errors}\n"
        out, retry = complete_json(msg, SCHEMA, prompt("tailor"), model)
        info = {**retry, "seconds": info["seconds"] + retry["seconds"]}
        doc = expand(to_selection(out, max_pages), ctx)  # a second failure goes to the caller
    write_resume(offer_dir / "resume.yaml", doc, "Written by `pipeline tailor` from context/ for offer.md.")
    return doc, info

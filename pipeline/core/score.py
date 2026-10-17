"""Score a resume against its offer: offer.md + resume.yaml -> score.md.

A model call separate from the writer, playing a recruiter screening for this role. It sees
only what the employer would see (the resume content), not context/.
"""

from __future__ import annotations

from pathlib import Path

from .llm import complete_json, prompt

_STR = {"type": "string"}


def _obj(**props) -> dict:
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


def _list(item: dict) -> dict:
    return {"type": "array", "items": item}


SCHEMA = _obj(
    score={"type": "number", "minimum": 0, "maximum": 10},
    verdict=_STR,
    weaknesses=_list(_STR),
    strengths=_list(_STR),
    requirements=_list(_obj(requirement=_STR, status={"type": "string", "enum": ["met", "partial", "missing"]}, evidence=_STR)),
    improvements=_list(_obj(
        action=_STR,
        kind={"type": "string", "enum": ["resume", "context", "skill"]},
        impact={"type": "string", "enum": ["high", "medium", "low"]},
    )),
)

_KIND = {
    "resume": "resume edit",
    "context": "add to context/ if true",
    "skill": "gap to close",
}
_STATUS = {"met": "✅", "partial": "⚠️", "missing": "❌"}


def _cell(s: str) -> str:
    return " ".join(s.split()).replace("|", "\\|") or "—"


def to_markdown(out: dict, offer_name: str, model: str) -> str:
    lines = [f"# Resume score: {out['score']:g}/10", "", f"_{offer_name}, scored by {model}_", "", out["verdict"], ""]
    lines += ["## Weaknesses", "", *(f"- {w}" for w in out["weaknesses"]), ""]
    lines += ["## Strengths", "", *(f"- {s}" for s in out["strengths"]), ""]
    lines += ["## Requirements", "", "| | Requirement | Evidence in the resume |", "|---|---|---|"]
    lines += [f"| {_STATUS[r['status']]} | {_cell(r['requirement'])} | {_cell(r['evidence'])} |" for r in out["requirements"]]
    lines += ["", "## To raise the score", ""]
    order = {"high": 0, "medium": 1, "low": 2}
    for imp in sorted(out["improvements"], key=lambda i: order[i["impact"]]):
        lines.append(f"- **{imp['impact']}** · {_KIND[imp['kind']]}: {imp['action']}")
    return "\n".join(lines) + "\n"


def score(offer_dir: Path, model: str | None = None) -> tuple[dict, dict]:
    """Write offer_dir/score.md; return (model output, run info)."""
    offer = (offer_dir / "offer.md").read_text(encoding="utf-8")
    resume = (offer_dir / "resume.yaml").read_text(encoding="utf-8")
    msg = f"# OFFER\n\n{offer}\n\n# RESUME (resume.yaml: exactly what the PDF shows)\n\n{resume}\n"
    out, info = complete_json(msg, SCHEMA, prompt("score"), model)
    (offer_dir / "score.md").write_text(to_markdown(out, offer_dir.name, info["model"]), encoding="utf-8")
    return out, info

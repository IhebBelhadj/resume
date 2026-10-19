"""Write a cover letter for an offer: context/ + offer.md (+ resume.yaml) + web research on the
company -> cover-letter.txt (plain text, the letter's body), with the research and its sources in
company.md. `letter_model` turns the .txt into the variables cover-letter.tex.j2 renders into the PDF."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

from .context import Context, dump_context
from .llm import complete_json, prompt
from .resume import LANGS, load_resume

LETTER_FILE = "cover-letter.txt"

TOOLS = ["WebSearch", "WebFetch"]
_STR = {"type": "string"}


def _obj(**props) -> dict:
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


SCHEMA = _obj(
    company=_STR,
    research={"type": "array", "items": _obj(fact=_STR, url=_STR)},
    letter=_STR,
)


def cover_letter(offer_dir: Path, ctx: Context, model: str | None = None) -> tuple[dict, dict]:
    """Write offer_dir/cover-letter.txt and company.md; return (model output, run info)."""
    offer = (offer_dir / "offer.md").read_text(encoding="utf-8")
    msg = f"# CONTEXT\n\n{dump_context(ctx)}\n\n# OFFER\n\n{offer}\n"
    if (resume := offer_dir / "resume.yaml").exists():
        msg += f"\n# RESUME SENT WITH THIS LETTER\n\n{resume.read_text(encoding='utf-8')}\n"
    out, info = complete_json(msg, SCHEMA, prompt("cover_letter"), model, tools=TOOLS)

    (offer_dir / LETTER_FILE).write_text(out["letter"].strip() + "\n", encoding="utf-8")
    research = "\n".join(f"- {r['fact']} ([source]({r['url']}))" for r in out["research"])
    (offer_dir / "company.md").write_text(
        f"# {out['company']}: research for the cover letter\n\n"
        f"_Found by {info['model']} on {dt.date.today().isoformat()}; check before sending._\n\n{research}\n",
        encoding="utf-8",
    )
    return out, info


_MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre",
              "octobre", "novembre", "décembre"]


def _date(d: dt.date, lang: str) -> str:
    return f"{d.day} {_MONTHS_FR[d.month - 1]} {d.year}" if lang == "fr" else f"{d.day} {d.strftime('%B %Y')}"


def letter_model(offer_dir: Path, profile: dict) -> dict:
    """cover-letter.txt -> the variables cover-letter.tex.j2 is rendered with. Header, language and
    company come from resume.yaml when it exists (so letter and resume match), else from `profile`."""
    text = (offer_dir / LETTER_FILE).read_text(encoding="utf-8")
    doc = load_resume(offer_dir / "resume.yaml") if (offer_dir / "resume.yaml").exists() else {}
    lang = doc.get("lang", "en") if doc.get("lang") in LANGS else "en"
    return {
        "lang": lang,
        "profile": doc.get("profile") or profile,
        "company": (doc.get("offer") or {}).get("company"),
        "date": _date(dt.date.today(), lang),
        # paragraphs are separated by a blank line; a line break inside one (the sign-off) is kept
        "paragraphs": [[ln.strip() for ln in b.splitlines() if ln.strip()] for b in text.split("\n\n") if b.strip()],
    }

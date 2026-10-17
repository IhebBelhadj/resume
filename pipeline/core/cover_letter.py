"""Write a cover letter for an offer: context/ + offer.md (+ resume.yaml) + web research on the
company -> cover-letter.md, with the research and its sources in company.md."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

from .context import Context, dump_context
from .llm import complete_json, prompt

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
    """Write offer_dir/cover-letter.md and company.md; return (model output, run info)."""
    offer = (offer_dir / "offer.md").read_text(encoding="utf-8")
    msg = f"# CONTEXT\n\n{dump_context(ctx)}\n\n# OFFER\n\n{offer}\n"
    if (resume := offer_dir / "resume.yaml").exists():
        msg += f"\n# RESUME SENT WITH THIS LETTER\n\n{resume.read_text(encoding='utf-8')}\n"
    out, info = complete_json(msg, SCHEMA, prompt("cover_letter"), model, tools=TOOLS)

    prof = ctx.profile
    contacts = " · ".join(c["label"] for c in prof["contacts"])
    (offer_dir / "cover-letter.md").write_text(
        f"**{prof['name']}**  \n{contacts}\n\n{dt.date.today().isoformat()}\n\n{out['letter'].strip()}\n",
        encoding="utf-8",
    )
    research = "\n".join(f"- {r['fact']} ([source]({r['url']}))" for r in out["research"])
    (offer_dir / "company.md").write_text(
        f"# {out['company']}: research for the cover letter\n\n"
        f"_Found by {info['model']} on {dt.date.today().isoformat()}; check before sending._\n\n{research}\n",
        encoding="utf-8",
    )
    return out, info

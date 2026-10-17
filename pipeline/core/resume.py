"""resume.yaml: everything the resume prints, so building it is deterministic.

`expand` turns a selection that references context/ by id (what the tailor model returns)
into a full resume document: profile, summary, skill groups and, for every entry, its
title, company, dates, bullets and stack, in render order. `build` then reads only
resume.yaml (`validate` + render), never context/.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from .context import Context

SECTIONS = ["summary", "skills", "experience", "projects", "education"]
LANGS = ("en", "fr")  # the resume is written in the offer's language; context/ is in English
# Jobs in these countries get the engineering-school degree names (prépa + diplôme d'ingénieur);
# everywhere else, their bachelor/master equivalents. See `names` in context/studies/*.md.
ENGINEERING_SYSTEM = {"TN", "FR"}
_ONGOING_RE = re.compile(r"(currently|present|now)\s*$", re.I)
_STR, _LIST = str, list
# required keys and their types, per entry list; checked by `validate`
_FIELDS = {
    "experiences": {"title": _STR, "company": _STR, "location": _STR, "dates": _STR, "bullets": _LIST, "stack": _LIST},
    "projects": {"name": _STR, "bullets": _LIST, "stack": _LIST},
    "education": {"degree": _STR, "school": _STR, "dates": _STR, "bullets": _LIST},
    "skills": {"label": _STR, "items": _LIST},
}


_CONCEPT_RE = re.compile(r"^(.+?)\s*\((.+)\)$")

# context/ display strings (dates, locations) are English; these translate their words
_WORDS = {
    "fr": {
        "January": "janv.", "Jan": "janv.", "February": "févr.", "Feb": "févr.", "March": "mars",
        "Mar": "mars", "April": "avr.", "Apr": "avr.", "May": "mai", "June": "juin", "Jun": "juin",
        "July": "juil.", "Jul": "juil.", "August": "août", "Aug": "août", "September": "sept.",
        "Sept": "sept.", "Sep": "sept.", "October": "oct.", "Oct": "oct.", "November": "nov.",
        "Nov": "nov.", "December": "déc.", "Dec": "déc.", "currently": "aujourd'hui",
        "Present": "aujourd'hui", "present": "aujourd'hui", "Remote": "à distance",
    },
}


def localize(s: str, lang: str) -> str:
    """Translate the English words of a context/ display string ("Oct 2025 – currently")."""
    words = _WORDS.get(lang)
    if not words:
        return s
    pattern = r"\b(" + "|".join(sorted(words, key=len, reverse=True)) + r")\b\.?"
    return re.sub(pattern, lambda m: words[m.group(1)], s)


def skill_error(item: str, known: set[str]) -> str | None:
    """A skill item is a known skill, or a concept backed by known skills: "Message brokers (Kafka)"."""
    if item in known:
        return None
    m = _CONCEPT_RE.match(item)
    if not m:
        return f"{item!r} not in skills.yaml (a concept must name the skills behind it: \"Concept (Skill, Skill)\")"
    unknown = [s.strip() for s in m.group(2).split(",") if s.strip() not in known]
    return f"{item!r}: {unknown} not in skills.yaml" if unknown else None


class ResumeError(ValueError):
    def __init__(self, errors: list[str]):
        super().__init__("\n".join(errors))
        self.errors = errors


def load_resume(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


class _Dumper(yaml.SafeDumper):
    pass


def _str(dumper, s):
    return dumper.represent_scalar("tag:yaml.org,2002:str", s, style=">" if len(s) > 90 else None)


def _list(dumper, xs):
    short = all(isinstance(x, str) and len(x) <= 40 for x in xs)
    return dumper.represent_sequence("tag:yaml.org,2002:seq", xs, flow_style=short)


_Dumper.add_representer(str, _str)
_Dumper.add_representer(list, _list)


def write_resume(path: Path, doc: dict, head: str) -> None:
    body = yaml.dump(doc, Dumper=_Dumper, sort_keys=False, allow_unicode=True, width=100)
    path.write_text(f"# {head}\n# Everything below is printed as-is by `pipeline build`; edit it here.\n" + body,
                    encoding="utf-8")


def validate(doc: dict) -> list[str]:
    """Shape errors that would make the template fail or print garbage."""
    errors = []
    if doc.get("lang", "en") not in LANGS:
        errors.append(f"lang: expected one of {LANGS}, got {doc.get('lang')!r}")
    prof = doc.get("profile") or {}
    if not isinstance(prof.get("name"), str) or not isinstance(prof.get("contacts"), list):
        errors.append("profile: needs `name` and `contacts`")
    if doc.get("summary") is not None and not isinstance(doc["summary"], str):
        errors.append("summary: must be a string (the text to print)")
    for s in doc.get("sections") or SECTIONS:
        if s not in SECTIONS:
            errors.append(f"sections: unknown section {s!r}")
    for key, fields in _FIELDS.items():
        for i, entry in enumerate(doc.get(key) or []):
            for f, typ in fields.items():
                if not isinstance(entry.get(f), typ):
                    errors.append(f"{key}[{i}].{f}: expected {typ.__name__}, got {entry.get(f)!r}")
            for j, b in enumerate(entry.get("bullets") or []):
                if not isinstance(b, str) or not b.strip():
                    errors.append(f"{key}[{i}].bullets[{j}]: expected a non-empty string")
    if not doc.get("experiences"):
        errors.append("experiences: none")
    return errors


def render_model(doc: dict) -> dict:
    """resume.yaml -> the variables resume.tex.j2 is rendered with."""
    errors = validate(doc)
    if errors:
        raise ResumeError(errors)
    return {
        "lang": doc.get("lang", "en"),
        "profile": doc["profile"],
        "sections": doc.get("sections") or SECTIONS,
        "summary": doc.get("summary"),
        "skills": doc.get("skills") or [],
        "experiences": doc["experiences"],
        "projects": [{"url": None, **p} for p in doc.get("projects") or []],
        "education": doc.get("education") or [],
    }


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


def expand(sel: dict, ctx: Context) -> dict:
    """Selection by id -> full resume document (raises ResumeError on unknown ids/skills)."""
    errors: list[str] = []
    lang = sel.get("lang", "en")
    if lang not in LANGS:
        errors.append(f"lang: expected one of {LANGS}, got {lang!r}")

    def bullets_for(entries, where: str) -> list[str]:
        for i, entry in enumerate(entries or []):
            if not isinstance(entry, str) or not entry.strip():
                errors.append(f"{where}.bullets[{i}]: expected a non-empty string, got {entry!r}")
        return [str(e) for e in entries or []]

    # summary: the text itself, written per offer
    summary_text = sel.get("summary")
    if summary_text is not None and not isinstance(summary_text, str):
        errors.append(f"summary: expected a string, got {summary_text!r}")
        summary_text = None

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
            if err := skill_error(it, ctx.all_skills):
                errors.append(f"skills[{i}] ({label}): {err}")
        skills.append({"label": label, "items": list(items)})

    # experiences: ongoing first, then newest first
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
        experiences.append(((bool(_ONGOING_RE.search(e["dates"])), str(e["start"])), {
            "title": title,
            "company": e["company"],
            "location": localize(e["location"], lang),
            "dates": localize(e["dates"], lang),
            "bullets": bullets_for(spec.get("bullets"), f"experiences.{eid}"),
            "stack": _stack(spec.get("stack"), e, ctx, f"experiences.{eid}", errors),
        }))
    experiences.sort(key=lambda x: x[0], reverse=True)

    # projects (keep selection order: most relevant first)
    projects = []
    for spec in sel.get("projects") or []:
        pid = spec["id"] if isinstance(spec, dict) else spec
        spec = spec if isinstance(spec, dict) else {}
        p = ctx.projects.get(pid)
        if not p:
            errors.append(f"projects: unknown id {pid!r}")
            continue
        projects.append({
            "name": p["name"],
            **({"url": p["url"]} if p.get("url") else {}),
            "bullets": bullets_for(spec.get("bullets"), f"projects.{pid}"),
            "stack": _stack(spec.get("stack", False), p, ctx, f"projects.{pid}", errors),
        })

    # education, newest first; degree name set by the job's country when the study has `names`
    system = "engineering" if (sel.get("offer") or {}).get("country", "").upper() in ENGINEERING_SYSTEM else "academic"
    education = []
    for spec in sel.get("education") or []:
        sid = spec["id"] if isinstance(spec, dict) else spec
        spec = spec if isinstance(spec, dict) else {}
        s = ctx.studies.get(sid)
        if not s:
            errors.append(f"education: unknown id {sid!r}")
            continue
        if names := (s.get("names") or {}).get(system):
            degree = names.get(lang) or names["en"]
        else:
            degree = spec.get("degree") or s["degrees"][0]
            if degree not in s["degrees"]:
                errors.append(f"education.{sid}: degree {degree!r} not in {s['degrees']}")
        education.append((str(s["start"]), {
            "degree": degree,
            "school": s["school"],
            "dates": localize(s["dates"], lang),
            "bullets": bullets_for(spec.get("bullets"), f"education.{sid}"),
        }))
    education.sort(key=lambda x: x[0], reverse=True)

    sections = sel.get("sections") or SECTIONS
    for s in sections:
        if s not in SECTIONS:
            errors.append(f"sections: unknown section {s!r}")
    if not experiences and not any(e.startswith("experiences") for e in errors):
        errors.append("experiences: none selected")
    if errors:
        raise ResumeError(errors)

    prof = ctx.profile
    doc = {
        "offer": sel.get("offer") or {},
        "lang": lang,
        "max_pages": sel.get("max_pages", 2),
        **({"sections": sections} if sel.get("sections") else {}),
        "profile": {"name": prof["name"], "pdf_name": prof.get("pdf_name", "resume"), "contacts": prof["contacts"]},
        "summary": " ".join(summary_text.split()) if summary_text else None,
        "skills": skills,
        "experiences": [e for _, e in experiences],
        "projects": projects,
        "education": [s for _, s in education],
    }
    if sel.get("gaps"):
        doc["gaps"] = sel["gaps"]
    return doc

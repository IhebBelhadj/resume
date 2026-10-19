"""Render resume.yaml into LaTeX using template/resume.tex.j2."""

from __future__ import annotations

import re

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from .context import ROOT

TEMPLATE_DIR = ROOT / "template"

_TEX_ESCAPES = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}
_ESC_RE = re.compile("|".join(re.escape(k) for k in _TEX_ESCAPES))
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def escape(s: str) -> str:
    return _ESC_RE.sub(lambda m: _TEX_ESCAPES[m.group()], s)


def url(u: str) -> str:
    return u.replace("%", r"\%").replace("#", r"\#")


def tex(s) -> str:
    """Escape plain text for LaTeX, supporting **bold** and [label](url)."""
    s = " ".join(str(s).split())
    links: list[str] = []

    def stash(m: re.Match) -> str:
        links.append(rf"\href{{{url(m.group(2))}}}{{{escape(m.group(1))}}}")
        return f"\x00{len(links) - 1}\x00"

    s = escape(_LINK_RE.sub(stash, s))
    s = _BOLD_RE.sub(r"\\textbf{\1}", s)
    return re.sub(r"\x00(\d+)\x00", lambda m: links[int(m.group(1))], s)


# printed headings, by resume.yaml `lang`
LABELS = {
    "en": {"resume": "Resume", "summary": "Summary", "skills": "Skills", "experience": "Experience",
           "projects": "Projects", "education": "Education", "stack": "Technologies used", "languages": "Spoken languages",
           "cover_letter": "Cover letter"},
    "fr": {"resume": "CV", "summary": "Profil", "skills": "Compétences",
           "experience": "Expérience professionnelle", "projects": "Projets", "education": "Formation",
           "stack": "Technologies utilisées", "languages": "Langues",
           "cover_letter": "Lettre de motivation"},
}


def _env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        block_start_string="<%",
        block_end_string="%>",
        variable_start_string="<<",
        variable_end_string=">>",
        comment_start_string="<#",
        comment_end_string="#>",
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        undefined=StrictUndefined,
        autoescape=False,
    )
    env.filters["tex"] = tex
    env.filters["url"] = url
    return env


def render_tex(model: dict, source_path: str, template: str = "resume.tex.j2") -> str:
    return _env().get_template(template).render(**model, t=LABELS[model["lang"]], source_path=source_path)

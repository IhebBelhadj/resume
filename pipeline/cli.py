"""Resume pipeline CLI.

    python -m pipeline check                 validate context/
    python -m pipeline dump                  all of context/ in one document (for LLM prompts)
    python -m pipeline new <slug>            scaffold offers/<slug>/offer.md
    python -m pipeline tailor <offer-dir>    context/ + offer.md -> resume.yaml (model), build + score, then
                                             one revision from the score's feedback (keeps the better)
    python -m pipeline build <offer-dir>...  resume.yaml (+ cover-letter.txt) -> .tex -> PDFs (no model)
    python -m pipeline score <offer-dir>     offer.md + resume.yaml -> score.md (model: x/10 + what to improve)
    python -m pipeline cover-letter <dir>    context/ + offer.md + web research -> cover-letter.txt + PDF, company.md
    python -m pipeline mark-sent <offer-dir> record as sent: commit offer files + PDF, tag sent/<slug>
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

import yaml

from .core.build import BuildError, compile_pdf
from .core.context import ROOT, ContextError, dump_context, load_context
from .core.cover_letter import LETTER_FILE, cover_letter, letter_model
from .core.llm import LLMError
from .core.render import render_tex
from .core.resume import ResumeError, load_resume, render_model
from .core.score import feedback, score
from .core.tailor import tailor

OFFERS_DIR = ROOT / "offers"


def cmd_check(_args) -> int:
    ctx = load_context()
    items = [*ctx.experiences.values(), *ctx.projects.values(), *ctx.studies.values()]
    def words(it: dict) -> int:
        return len(re.sub(r"<!--.*?-->", "", it["raw"], flags=re.S).split())

    total = sum(words(it) for it in items)
    print(
        f"ok: {len(ctx.experiences)} experiences, {len(ctx.projects)} projects, {len(ctx.studies)} studies "
        f"({total} words of raw facts), {len(ctx.all_skills)} skills"
    )
    for it in items:
        n = words(it)
        todos = sum(str(v).count("TODO") for k, v in it.items() if not k.startswith("_"))
        if n < 80 or todos:
            print(f"  thin: {it['_path']} ({n} words" + (f", {todos} TODO" if todos else "") + ")")
    return 0


def cmd_dump(_args) -> int:
    print(dump_context(load_context()))
    return 0


def cmd_new(args) -> int:
    d = OFFERS_DIR / args.slug
    if d.exists():
        print(f"error: {d} already exists", file=sys.stderr)
        return 1
    d.mkdir(parents=True)
    (d / "offer.md").write_text(
        "---\ncompany:\nrole:\nurl:\nfetched: \n---\n\n<!-- paste the job description here -->\n",
        encoding="utf-8",
    )
    print(f"created {d.relative_to(ROOT)}/offer.md; paste the offer, then `pipeline tailor {d.relative_to(ROOT)}`")
    return 0


def build_one(offer_dir: Path, force: bool = False) -> int:
    res_path = offer_dir / "resume.yaml"
    if not res_path.exists():
        print(f"[{offer_dir.name}] no resume.yaml; run `pipeline tailor` first", file=sys.stderr)
        return 1
    doc = load_resume(res_path)
    if doc.get("sent") and not force:
        print(f"[{offer_dir.name}] skipped: sent on {doc['sent']}; its PDF is the record (use --force to rebuild)")
        return 0
    try:
        model = render_model(doc)
    except ResumeError as e:
        print(f"[{offer_dir.name}] resume.yaml invalid:", file=sys.stderr)
        for err in e.errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    tex_path = offer_dir / "resume.tex"
    tex_path.write_text(render_tex(model, str(res_path.relative_to(ROOT))), encoding="utf-8")
    try:
        result = compile_pdf(tex_path, doc["profile"].get("pdf_name", "resume"))
    except BuildError as e:
        print(e, file=sys.stderr)
        return 1

    max_pages = doc.get("max_pages", 2)
    print(f"[{offer_dir.name}] {result.pdf.relative_to(ROOT)}: {result.pages} page(s)")
    if result.pages > max_pages:
        print(f"  FAIL: exceeds max_pages={max_pages}; drop or shorten bullets in resume.yaml", file=sys.stderr)
        return 2
    if (offer_dir / LETTER_FILE).exists():
        return build_letter(offer_dir, doc["profile"])
    return 0


def _letter_pdf_name(profile: dict) -> str:
    return f"{profile.get('pdf_name', 'resume')}_COVER_LETTER"


def build_letter(offer_dir: Path, profile: dict) -> int:
    """cover-letter.txt -> cover-letter.tex -> PDF (one page)."""
    model = letter_model(offer_dir, profile)
    tex_path = offer_dir / "cover-letter.tex"
    tex_path.write_text(render_tex(model, str((offer_dir / LETTER_FILE).relative_to(ROOT)), "cover-letter.tex.j2"),
                        encoding="utf-8")
    try:
        result = compile_pdf(tex_path, _letter_pdf_name(model["profile"]))
    except BuildError as e:
        print(e, file=sys.stderr)
        return 1
    print(f"[{offer_dir.name}] {result.pdf.relative_to(ROOT)}: {result.pages} page(s)")
    if result.pages > 1:
        print(f"  FAIL: the cover letter must fit on one page; shorten {LETTER_FILE}", file=sys.stderr)
        return 2
    return 0


def cmd_build(args) -> int:
    dirs = [Path(p).resolve() for p in args.offers] or sorted(p for p in OFFERS_DIR.iterdir() if p.is_dir())
    return max((build_one(d, args.force) for d in dirs), default=0)


def _offer_dir(arg: str, writes: str) -> Path | None:
    """Resolve an offer dir; None (with an error printed) if offer.md is missing or it was sent."""
    d = Path(arg).resolve()
    if not (d / "offer.md").exists():
        print(f"error: {d}/offer.md missing; run `pipeline new <slug>` and paste the offer", file=sys.stderr)
        return None
    if writes and (d / "resume.yaml").exists() and load_resume(d / "resume.yaml").get("sent"):
        print(f"error: {d.name} was sent; {writes} would change its record. Create a new offer folder.", file=sys.stderr)
        return None
    return d


def _run(info: dict) -> str:
    return f"{info['model']}, {info['seconds']:.0f}s"


def _score(offer_dir: Path, model: str | None) -> dict:
    print(f"[{offer_dir.name}] scoring resume.yaml against offer.md...", flush=True)
    out, info = score(offer_dir, model)
    print(f"[{offer_dir.name}] score {out['score']:g}/10 -> {(offer_dir / 'score.md').relative_to(ROOT)} ({_run(info)})")
    return out


def _write(offer_dir: Path, ctx, args, max_pages: int, notes: str | None = None) -> dict | None:
    """One tailor call; prints gaps. None (errors printed) if the model's answer was rejected twice."""
    what = "revising resume.yaml from the score's feedback" if notes else "writing resume.yaml"
    print(f"[{offer_dir.name}] {what}...", flush=True)
    try:
        doc, info = tailor(offer_dir, ctx, args.model, max_pages, notes)
    except ResumeError as e:
        print(f"[{offer_dir.name}] the model's answer was rejected twice (re-run tailor):", file=sys.stderr)
        for err in e.errors:
            print(f"  - {err}", file=sys.stderr)
        return None
    print(f"[{offer_dir.name}] wrote {(offer_dir / 'resume.yaml').relative_to(ROOT)} ({_run(info)})")
    if doc.get("gaps"):
        print("  gaps (offer asks, context lacks; add to context/ if true, then re-run):")
        for g in doc["gaps"]:
            print(f"    - {g}")
    return doc


def cmd_tailor(args) -> int:
    if not (offer_dir := _offer_dir(args.offer, "tailor")):
        return 1
    res_path = offer_dir / "resume.yaml"
    max_pages = args.max_pages or (load_resume(res_path).get("max_pages", 2) if res_path.exists() else 2)
    ctx = load_context()
    if _write(offer_dir, ctx, args, max_pages) is None:
        return 1
    status = build_one(offer_dir)
    if status != 0 or args.no_score:
        return status
    first = _score(offer_dir, args.model)
    if args.no_revise:
        return 0

    # One revision: the writer gets the reviewer's notes. Keep whichever version scores higher.
    kept = {p: (offer_dir / p).read_text(encoding="utf-8") for p in ("resume.yaml", "score.md")}
    revised = _write(offer_dir, ctx, args, max_pages, feedback(first))
    status = build_one(offer_dir) if revised is not None else 1
    second = _score(offer_dir, args.model) if status == 0 else None
    if second is not None and second["score"] >= first["score"]:
        print(f"[{offer_dir.name}] revision kept: {first['score']:g} -> {second['score']:g}/10")
        return 0
    why = f"it scored {second['score']:g} < {first['score']:g}" if second else "it failed"
    print(f"[{offer_dir.name}] revision discarded ({why}); restoring the first version")
    for p, text in kept.items():
        (offer_dir / p).write_text(text, encoding="utf-8")
    return build_one(offer_dir)


def cmd_score(args) -> int:
    if not (offer_dir := _offer_dir(args.offer, "")):
        return 1
    if not (offer_dir / "resume.yaml").exists():
        print(f"error: {offer_dir.name} has no resume.yaml; run `pipeline tailor` first", file=sys.stderr)
        return 1
    _score(offer_dir, args.model)
    return 0


def cmd_cover_letter(args) -> int:
    if not (offer_dir := _offer_dir(args.offer, "cover-letter")):
        return 1
    print(f"[{offer_dir.name}] researching the company and writing the cover letter...", flush=True)
    ctx = load_context()
    out, info = cover_letter(offer_dir, ctx, args.model)
    print(f"[{offer_dir.name}] {(offer_dir / LETTER_FILE).relative_to(ROOT)} "
          f"({len(out['letter'].split())} words, {len(out['research'])} researched facts in company.md; {_run(info)})")
    return build_letter(offer_dir, ctx.profile)


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)


def cmd_mark_sent(args) -> int:
    offer_dir = Path(args.offer).resolve()
    slug = offer_dir.name
    res_path = offer_dir / "resume.yaml"
    doc = load_resume(res_path)
    pdf = offer_dir / f"{(doc.get('profile') or {}).get('pdf_name', 'resume')}.pdf"
    tag = f"sent/{slug}"

    if doc.get("sent"):
        print(f"error: {slug} already marked sent on {doc['sent']}", file=sys.stderr)
        return 1
    if not pdf.exists():
        print(f"error: {pdf.relative_to(ROOT)} missing; run build first", file=sys.stderr)
        return 1
    if res_path.stat().st_mtime > pdf.stat().st_mtime:
        print("error: resume.yaml is newer than the PDF; rebuild first so the PDF matches", file=sys.stderr)
        return 1
    if _git("rev-parse", "-q", "--verify", f"refs/tags/{tag}").returncode == 0:
        print(f"error: tag {tag} already exists", file=sys.stderr)
        return 1

    letter_pdf = offer_dir / f"{_letter_pdf_name(doc.get('profile') or {})}.pdf"
    if (offer_dir / LETTER_FILE).exists() and (
            not letter_pdf.exists() or (offer_dir / LETTER_FILE).stat().st_mtime > letter_pdf.stat().st_mtime):
        print(f"error: {LETTER_FILE} is newer than its PDF; rebuild first so the PDF matches", file=sys.stderr)
        return 1

    date = args.date or dt.date.today().isoformat()
    # Insert/replace a top-level `sent:` line without rewriting the file (keeps comments).
    text = res_path.read_text(encoding="utf-8")
    line = f"sent: {date}\n"
    text, n = re.subn(r"^sent:.*\n", line, text, flags=re.M)
    if not n:
        text = line + text
    res_path.write_text(text, encoding="utf-8")
    pdf.touch()  # keep the PDF newer than resume.yaml

    paths = [str(p.relative_to(ROOT)) for p in (offer_dir / "offer.md", res_path, offer_dir / "resume.tex", pdf,
                                                     offer_dir / LETTER_FILE, offer_dir / "cover-letter.tex", letter_pdf,
                                                     offer_dir / "company.md", offer_dir / "score.md") if p.exists()]
    company = (doc.get("offer") or {}).get("company") or slug
    steps = [
        ("add", "-f", "--", *paths),  # -f: offer PDFs are gitignored until sent
        ("commit", "-m", f"sent: {company} ({slug})", "--only", "--", *paths),
        ("tag", "-a", tag, "-m", f"Resume sent to {company} on {date}"),
    ]
    for step in steps:
        r = _git(*step)
        if r.returncode != 0:
            print(f"error: git {step[0]} failed:\n{r.stderr or r.stdout}", file=sys.stderr)
            return 1
    print(f"[{slug}] marked sent on {date}: committed {len(paths)} file(s), tagged {tag}")
    print(f"  push with: git push && git push origin {tag}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="pipeline", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check").set_defaults(fn=cmd_check)
    sub.add_parser("dump").set_defaults(fn=cmd_dump)
    p = sub.add_parser("new")
    p.add_argument("slug", help="e.g. 2026-10-acme-backend")
    p.set_defaults(fn=cmd_new)
    p = sub.add_parser("build")
    p.add_argument("offers", nargs="*", help="offer dirs (default: all under offers/)")
    p.add_argument("--force", action="store_true", help="rebuild offers already marked sent")
    p.set_defaults(fn=cmd_build)
    p = sub.add_parser("tailor")
    p.add_argument("offer", help="offer dir containing offer.md")
    p.add_argument("--model", help="claude model alias or id (default: $RESUME_MODEL or opus)")
    p.add_argument("--max-pages", type=int, help="page budget (default: the existing resume.yaml's, else 2)")
    p.add_argument("--no-score", action="store_true", help="skip scoring after the build (implies --no-revise)")
    p.add_argument("--no-revise", action="store_true", help="skip the revision from the score's feedback")
    p.set_defaults(fn=cmd_tailor)
    p = sub.add_parser("score")
    p.add_argument("offer", help="offer dir with offer.md and resume.yaml")
    p.add_argument("--model", help="claude model alias or id (default: $RESUME_MODEL or opus)")
    p.set_defaults(fn=cmd_score)
    p = sub.add_parser("cover-letter")
    p.add_argument("offer", help="offer dir with offer.md (uses resume.yaml too if present)")
    p.add_argument("--model", help="claude model alias or id (default: $RESUME_MODEL or opus)")
    p.set_defaults(fn=cmd_cover_letter)
    p = sub.add_parser("mark-sent")
    p.add_argument("offer", help="offer dir, e.g. offers/2026-10-acme-backend")
    p.add_argument("--date", help="YYYY-MM-DD (default: today)")
    p.set_defaults(fn=cmd_mark_sent)
    args = ap.parse_args(argv)
    try:
        return args.fn(args)
    except (ContextError, yaml.YAMLError) as e:
        print(f"context error: {e}", file=sys.stderr)
        return 1
    except LLMError as e:
        print(f"model error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

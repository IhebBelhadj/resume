"""Resume pipeline CLI.

    python -m pipeline check                 validate context/
    python -m pipeline dump                  compact, id-annotated view of context/ (for LLM prompts)
    python -m pipeline new <slug>            scaffold offers/<slug>/
    python -m pipeline build <offer-dir>...  selection.yaml -> resume.tex -> PDF + checks
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

from .core.build import BuildError, compile_pdf, keyword_coverage
from .core.context import ROOT, ContextError, load_context
from .core.render import render_tex
from .core.selection import SelectionError, load_selection, resolve

OFFERS_DIR = ROOT / "offers"


def cmd_check(_args) -> int:
    ctx = load_context()
    print(
        f"ok: {len(ctx.experiences)} experiences, {len(ctx.projects)} projects, "
        f"{len(ctx.studies)} studies, {len(ctx.bullets)} bullets, {len(ctx.summaries)} summaries, "
        f"{len(ctx.all_skills)} skills"
    )
    return 0


def cmd_dump(_args) -> int:
    """One compact document with every id the selection can reference."""
    ctx = load_context()
    out: list[str] = ["# SUMMARIES"]
    for s in ctx.summaries.values():
        out.append(f"- {s['id']} [{', '.join(s.get('tags', []))}]: {' '.join(s['text'].split())}")
    out.append("\n# SKILLS (category id: items)")
    for c in ctx.skills:
        out.append(f"- {c['id']} ({c['label']}): {', '.join(c['items'])}")

    def dump_items(title: str, items: dict, head) -> None:
        out.append(f"\n# {title}")
        for it in sorted(items.values(), key=lambda x: str(x.get("start", "")), reverse=True):
            out.append(f"\n## {it['id']}: {head(it)}")
            if it.get("stack"):
                out.append(f"stack: {', '.join(it['stack'])}")
            for b in it.get("bullets") or []:
                v = f" (variant_of {b['variant_of']})" if b.get("variant_of") else ""
                out.append(f"- {b['id']}{v} [{', '.join(b.get('tags', []))}]: {' '.join(b['text'].split())}")
            if it.get("notes"):
                out.append("notes: " + " ".join(it["notes"].split()))

    dump_items("EXPERIENCES", ctx.experiences,
               lambda e: f"{' | '.join(e['titles'])} @ {e['company']}, {e['location']} ({e['dates']})")
    dump_items("PROJECTS", ctx.projects, lambda p: f"{p['name']} <{p.get('url', '')}>")
    dump_items("STUDIES", ctx.studies, lambda s: f"{' | '.join(s['degrees'])} @ {s['school']} ({s['dates']})")
    if ctx.profile.get("notes"):
        out.append("\n# PROFILE NOTES\n" + ctx.profile["notes"].strip())
    print("\n".join(out))
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
    (d / "selection.yaml").write_text((ROOT / "template" / "selection.example.yaml").read_text(), encoding="utf-8")
    print(f"created {d.relative_to(ROOT)}/ (offer.md, selection.yaml)")
    return 0


def build_one(offer_dir: Path, force: bool = False) -> int:
    sel_path = offer_dir / "selection.yaml"
    sel = load_selection(sel_path)
    if sel.get("sent") and not force:
        print(f"[{offer_dir.name}] skipped: sent on {sel['sent']}; its PDF is the record (use --force to rebuild)")
        return 0
    ctx = load_context()
    try:
        res = resolve(sel, ctx)
    except SelectionError as e:
        print(f"[{offer_dir.name}] selection invalid:", file=sys.stderr)
        for err in e.errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    tex_path = offer_dir / "resume.tex"
    tex_path.write_text(render_tex(res.model, str(sel_path.relative_to(ROOT))), encoding="utf-8")
    try:
        result = compile_pdf(tex_path, ctx.profile.get("pdf_name", "resume"))
    except BuildError as e:
        print(e, file=sys.stderr)
        return 1

    max_pages = sel.get("max_pages", 1)
    status = 0
    print(f"[{offer_dir.name}] {result.pdf.relative_to(ROOT)}: {result.pages} page(s)")
    if result.pages > max_pages:
        print(f"  FAIL: exceeds max_pages={max_pages}; drop or shorten bullets", file=sys.stderr)
        status = 2
    for w in res.warnings:
        print(f"  warn: {w}")
    if res.rewrites:
        print(f"  {len(res.rewrites)} rewrite(s) to review (must not add facts):")
        for bid, orig, new in res.rewrites:
            print(f"    - {bid}:\n        was: {' '.join(orig.split())}\n        now: {' '.join(new.split())}")
    if kws := sel.get("keywords"):
        found, missing = keyword_coverage(result.text, kws)
        print(f"  keywords: {len(found)}/{len(kws)} present" + (f"; missing: {', '.join(missing)}" if missing else ""))
    return status


def cmd_build(args) -> int:
    dirs = [Path(p).resolve() for p in args.offers] or sorted(p for p in OFFERS_DIR.iterdir() if p.is_dir())
    return max((build_one(d, args.force) for d in dirs), default=0)


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)


def cmd_mark_sent(args) -> int:
    offer_dir = Path(args.offer).resolve()
    slug = offer_dir.name
    sel_path = offer_dir / "selection.yaml"
    sel = load_selection(sel_path)
    pdf = offer_dir / f"{load_context().profile.get('pdf_name', 'resume')}.pdf"
    tag = f"sent/{slug}"

    if sel.get("sent"):
        print(f"error: {slug} already marked sent on {sel['sent']}", file=sys.stderr)
        return 1
    if not pdf.exists():
        print(f"error: {pdf.relative_to(ROOT)} missing; run build first", file=sys.stderr)
        return 1
    if sel_path.stat().st_mtime > pdf.stat().st_mtime:
        print("error: selection.yaml is newer than the PDF; rebuild first so the PDF matches", file=sys.stderr)
        return 1
    if _git("rev-parse", "-q", "--verify", f"refs/tags/{tag}").returncode == 0:
        print(f"error: tag {tag} already exists", file=sys.stderr)
        return 1

    date = args.date or dt.date.today().isoformat()
    # Insert/replace a top-level `sent:` line without rewriting the file (keeps comments).
    text = sel_path.read_text(encoding="utf-8")
    line = f"sent: {date}\n"
    text, n = re.subn(r"^sent:.*\n", line, text, flags=re.M)
    if not n:
        text = line + text
    sel_path.write_text(text, encoding="utf-8")
    pdf.touch()  # keep the PDF newer than selection.yaml

    paths = [str(p.relative_to(ROOT)) for p in (offer_dir / "offer.md", sel_path, offer_dir / "resume.tex", pdf) if p.exists()]
    company = (sel.get("offer") or {}).get("company") or slug
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


if __name__ == "__main__":
    sys.exit(main())

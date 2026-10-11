# Resume pipeline

Generates a resume tailored to each job offer from a structured knowledge base about Iheb.
Content (facts) is kept apart from presentation (LaTeX): the agent *selects* from
`context/`, a renderer turns that selection into LaTeX, and `latexmk` compiles it.

```
context/        SOURCE OF TRUTH: every fact about Iheb (YAML, id-annotated). See context/CLAUDE.md
template/       resume.cls (all styling), resume.tex.j2 (Jinja2 layout), selection.example.yaml
offers/<slug>/  one folder per offer: offer.md, selection.yaml, resume.tex (generated), <pdf_name>.pdf
pipeline/core/  pure Python (no orchestrator imports): context loading, selection validation, render, build
pipeline/flows/ orchestration wrappers only (Prefect, phase 3)
build/          latexmk aux files (gitignored)
legacy/         old hand-written .tex/.pdf variants, kept for reference until the pipeline is trusted
```

## Commands

Always use the project venv (`python3 -m venv .venv && .venv/bin/pip install -e .` if missing).

```sh
.venv/bin/python -m pipeline check                  # validate context/ (ids, variants, required keys)
.venv/bin/python -m pipeline dump                   # compact id-annotated view of ALL context (~3k tokens)
.venv/bin/python -m pipeline new 2026-10-acme-backend
.venv/bin/python -m pipeline build offers/<slug>    # validate selection -> resume.tex -> PDF -> checks
.venv/bin/python -m pipeline build                  # rebuild every offer (skips ones marked sent)
.venv/bin/python -m pipeline mark-sent offers/<slug> [--date YYYY-MM-DD]
```

## What goes in git

- Always: `context/`, `template/`, `pipeline/`, and per offer `offer.md`, `selection.yaml`, `resume.tex`.
- Offer PDFs are gitignored (`offers/*/*.pdf`) **until sent**. `mark-sent` checks that the PDF
  is newer than `selection.yaml`, writes `sent: <date>` into it, force-adds the PDF, commits
  only that offer's files (other staged changes are left alone), and tags `sent/<slug>`.
  The user pushes (`git push && git push origin sent/<slug>`).
- A sent offer is frozen: `build` skips it unless `--force`, because its committed PDF is
  the record of what the company received. Never rebuild or edit a sent offer; for a new
  version of an application, create a new offer folder.
- The repo holds personal data (phone, email) and where the user applies: keep it private.

`build` exits non-zero if the selection references unknown ids/skills, if LaTeX errors,
or if the PDF exceeds `max_pages`. It reports variant clashes, rewrites to review, and
keyword coverage (from `keywords:` in selection.yaml, checked against the PDF text).

## Hard rules for any agent tailoring a resume

1. **Never invent facts.** Every experience, bullet, project, skill, metric, date and title
   must come from `context/`. If the offer asks for something that is not there, report
   it as a *gap*; do not add it. Do not inflate levels ("familiar" never becomes "expert").
2. **Select by id, don't write LaTeX.** The only output is `offers/<slug>/selection.yaml`.
   Never hand-edit `resume.tex` (it is regenerated) and never put styling in it.
3. **Rewrites are allowed only to reword.** A `{id, text}` rewrite may reorder, shorten, or
   mirror the offer's vocabulary for something the original bullet already says. It must
   not add technologies, numbers, scope or responsibility. `build` lists every rewrite for
   human review.
4. **Pick one variant.** Bullets with `variant_of` are alternative phrasings of the same
   fact; use at most one per group.
5. **Fit the page budget.** Default `max_pages: 1`. Drop the least relevant bullets and
   projects first; then trim stacks; then shorten via rewrites.
6. **New facts go to `context/` first**, with the user's confirmation, never straight
   into a selection.

## Tailoring workflow (interactive: `/tailor-resume`)

offer → `offers/<slug>/offer.md` → extract must-haves / nice-to-haves / keywords →
`pipeline dump` → choose summary, skills (offer-relevant first), experiences, bullets,
projects → write `selection.yaml` → `pipeline build` → fix until it passes → report coverage,
gaps and rewrites. Slug format: `YYYY-MM-<company>-<role>` (kebab-case).

## Token efficiency

- Read context via `pipeline dump` (one call) instead of opening every YAML file.
- Only open a project's repo (`repo:` in its context file, readable through
  `additionalDirectories` in `.claude/settings.json`) when the offer needs detail the context
  file lacks, and then *update the context file* so the next run doesn't need the repo.
- Use `/ingest-project <path>` to turn a repo into a context file once.

## Architecture decisions (keep these)

- **LaTeX via Jinja2**, delimiters `<< >>`, `<% %>`, `<# #>` so they don't clash with LaTeX.
  All free text goes through the `tex` filter (escapes LaTeX, supports `**bold**` and
  `[label](url)`). Layout changes go in `resume.cls` / `resume.tex.j2`, never per-offer.
- **Selection = ids + optional rewrites** so output is verifiable in code (no hallucinated
  bullets) and cheap to produce (small structured output, no agent loop needed).
- **`core/` vs `flows/` split.** `pipeline/core` must never import an orchestrator. Prefect
  is the first orchestrator; switching to Dagster later means rewriting only `flows/`.
- Experiences and education render newest-first automatically (by `start`); projects render
  in selection order (most relevant first).

## Roadmap

1. ✅ Foundation: context/ KB, resume.cls, Jinja renderer, validator, build checks, generic baseline.
2. ⏳ Fill context gaps (TODOs in context files), ingest project repos, port the legacy
   devops/java/frontend/nextjs variants into `offers/` selections.
3. ⏳ Automation (Prefect, `pipeline/flows/`): fetch offers (RSS / email alerts / pasted URLs;
   trafilatura or Crawl4AI; no scraping of sites whose ToS forbid it) → SQLite dedupe
   (`pipeline/state/`) → cheap fit filter (small model) → tailor via Anthropic API with
   structured output producing `selection.yaml` (prompt-cache the `pipeline dump` prefix; Batch
   API for nightly runs) → `pipeline build` → notify (ntfy/Telegram). A human reviews every
   resume before it is sent; never auto-apply.

# Resume pipeline

Generates a resume tailored to each job offer from a structured knowledge base about Iheb.
Content (facts) is kept apart from presentation (LaTeX). Per offer:

1. **tailor**: one model call reads the `context/` Markdown files and `offer.md`, picks the
   entries and writes the summary and bullets; code copies the rest (titles, dates, contacts…) from
   `context/` and writes `resume.yaml`, which holds **everything the resume prints**.
2. **build** (deterministic, no model, never reads `context/`): Jinja2 fills
   `template/resume.tex.j2` from `resume.yaml` into `resume.tex`; `latexmk` makes the PDF.
3. **score**: a separate model call reads `offer.md` + `resume.yaml` and writes `score.md`
   (fit out of 10, weaknesses, requirement table, what to do to raise the score).
   **Revision (once):** `tailor` then runs again with the previous `resume.yaml` and the score's
   feedback (weaknesses + resume edits; requests for new facts stay gaps), builds and re-scores;
   the higher-scoring version is kept (`--no-revise` skips it).
4. **cover-letter** (on demand): a model call with web search researches the company and
   writes the letter's body as plain text in `cover-letter.txt` from `context/` + the offer +
   `resume.yaml`; the facts it found, with source URLs, go to `company.md`. `build` renders the
   .txt through `template/cover-letter.tex.j2` (`letter.cls`, same header as the resume) into
   `cover-letter.tex` and `<pdf_name>_COVER_LETTER.pdf` (one page; header, language and company
   come from `resume.yaml`). Edit the .txt by hand, then `build`.

Models run through the local Claude Code CLI (`claude -p`, the user's subscription; no API key).

```
context/        SOURCE OF TRUTH: every fact about Iheb (Markdown + YAML frontmatter). See context/CLAUDE.md
template/       resume.cls (all styling), resume.tex.j2 (Jinja2 layout), resume.example.yaml (format),
                letter.cls + cover-letter.tex.j2 (cover letter), _header.tex.j2 (shared header)
offers/<slug>/  one folder per offer: offer.md, resume.yaml, resume.tex, <pdf_name>.pdf, score.md,
                cover-letter.txt, cover-letter.tex, <pdf_name>_COVER_LETTER.pdf, company.md
pipeline/core/  pure Python (no orchestrator imports): context, resume, render, build, llm (claude -p),
                tailor, score, cover_letter
pipeline/core/prompts/  system prompts: tailor, score, cover_letter
pipeline/flows/ orchestration wrappers only (Prefect, phase 3)
build/          latexmk aux files (gitignored)
legacy/         old hand-written .tex/.pdf variants, kept for reference until the pipeline is trusted
```

## Commands

Always use the project venv (`python3 -m venv .venv && .venv/bin/pip install -e .` if missing).

```sh
.venv/bin/python -m pipeline check                  # validate context/ (ids, required keys); lists thin files
.venv/bin/python -m pipeline dump                   # ALL context in one document (frontmatter + raw facts)
.venv/bin/python -m pipeline new 2026-10-acme-backend   # creates offer.md
.venv/bin/python -m pipeline tailor offers/<slug>   # -> resume.yaml, build, score, 1 revision (--max-pages N, --no-score, --no-revise)
.venv/bin/python -m pipeline build offers/<slug>    # resume.yaml (+ cover-letter.txt) -> .tex -> PDFs (no model)
.venv/bin/python -m pipeline build                  # rebuild every offer (skips ones marked sent)
.venv/bin/python -m pipeline score offers/<slug>    # -> score.md
.venv/bin/python -m pipeline cover-letter offers/<slug>   # -> cover-letter.txt + PDF, company.md (web research)
.venv/bin/python -m pipeline mark-sent offers/<slug> [--date YYYY-MM-DD]
```

## What goes in git

- Always: `context/`, `template/`, `pipeline/`, and per offer `offer.md`, `resume.yaml`, `resume.tex`,
  `score.md`, `cover-letter.txt`, `cover-letter.tex`, `company.md`.
- Offer PDFs are gitignored (`offers/*/*.pdf`) **until sent**. `mark-sent` checks that each PDF
  is newer than its source (`resume.yaml`, `cover-letter.txt`), writes `sent: <date>` into `resume.yaml`, force-adds the PDFs, commits
  only that offer's files (other staged changes are left alone), and tags `sent/<slug>`.
  The user pushes (`git push && git push origin sent/<slug>`).
- A sent offer is frozen: `build` skips it unless `--force`, because its committed PDF is
  the record of what the company received. Never rebuild or edit a sent offer; for a new
  version of an application, create a new offer folder.
- The repo holds personal data (phone, email) and where the user applies: keep it private.

`tailor` fails if the model references ids/skills not in `context/`, and prints the offer's
gaps (asked for, not in `context/`). `build` fails if `resume.yaml` is malformed, LaTeX
errors, or the PDF exceeds `max_pages`. `tailor` and `cover-letter` refuse a sent offer.
Model: `--model` or `$RESUME_MODEL` (default `opus`).

## Hard rules for any agent tailoring a resume

1. **Never invent facts.** Every experience, bullet, project, skill, metric, date and title
   must come from `context/`. If the offer asks for something that is not there, report
   it as a *gap*; do not add it. Do not inflate levels ("familiar" never becomes "expert").
   Concepts transfer, tool names don't: when the offer wants a tool Iheb hasn't used but
   `context/` shows the same concept with another one, pitch the concept in the offer's
   terms and name the real tool ("Message brokers (Kafka)" for an offer asking RabbitMQ);
   `tailor` checks that every technology named is in `skills.yaml`.
2. **Write `resume.yaml`, not LaTeX.** The resume's only source is `offers/<slug>/resume.yaml`
   (normally written by `pipeline tailor`; hand edits follow the same rules: titles,
   dates and contacts as in `context/`).
   Never hand-edit `resume.tex` (it is regenerated) and never put styling in it.
3. **Every bullet stays within its context file.** Bullets are plain strings, written for
   the offer from the body of the owning context file. They may reorder, combine, shorten
   and use the offer's vocabulary, but must claim nothing the body doesn't: no added
   technologies, numbers, scope, seniority or ownership ("used" never becomes "led",
   "contributed to" never becomes "built").
4. **Balance the bullets.** About 14–16 in total; at most 5 per experience, and only the most
   relevant one gets 4–5, the others compensate (2–3, then 1); every experience longer than
   4 months (`resume.MIN_BULLET_MONTHS`) gets at least one bullet saying what the role was,
   even if unrelated to the offer (`tailor` rejects it otherwise and retries once); projects 0–2, one line each, or up to 3
   bullets for a project that is among the most relevant (printed nested under its name).
   `tailor` caps bullets per entry in its output schema.
5. **One or two pages, by content.** `max_pages: 2` is a ceiling, not a target: one page
   when the relevant material fits, two when there is enough relevant material to fill a
   good part of the second; never pad to fill it. Over budget: drop the least relevant
   bullets and projects first; then trim stacks; then shorten bullets.
6. **Match the offer's language.** `lang` (`en` | `fr`) in `resume.yaml`: the model writes
   the summary, bullets and skill labels in the offer's language; code translates headings
   (`render.LABELS`) and context dates/locations (`resume.localize`). Titles and degrees
   come from `context/` (add a translated variant to `titles`/`degrees` to use it).
7. **New facts go to `context/` first**, with the user's confirmation, never straight
   into a `resume.yaml`. The same goes for cover letters.

## Tailoring workflow (interactive: `/tailor-resume`)

offer → `pipeline new <slug>` → paste it into `offer.md` → `pipeline tailor offers/<slug>`
(writes resume.yaml, builds the PDF, scores it) → report score, coverage and gaps → for gaps
the user confirms, add the facts to `context/` and re-run `tailor` → `pipeline cover-letter`
if the application wants one.
Slug format: `YYYY-MM-<company>-<role>` (kebab-case).

## Token efficiency

- Read context via `pipeline dump` (one call) instead of opening every context file.
- Only open a project's repo (`repo:` in its context file, readable through
  `additionalDirectories` in `.claude/settings.json`) when the offer needs detail the context
  file lacks, and then *update the context file* so the next run doesn't need the repo.
- Use `/ingest-project <path>` to turn a repo into a context file once.

## Architecture decisions (keep these)

- **LaTeX via Jinja2**, delimiters `<< >>`, `<% %>`, `<# #>` so they don't clash with LaTeX.
  All free text goes through the `tex` filter (escapes LaTeX, supports `**bold**` and
  `[label](url)`). Layout changes go in `resume.cls` / `resume.tex.j2`, never per-offer.
- **Context = Markdown with YAML frontmatter.** Frontmatter holds what code validates and
  renders (ids, titles, dates, stack); the body is a free-form fact dump, as complete as
  possible, never rendered.
- **`resume.yaml` is the complete resume.** The model never writes dates, titles or
  contacts (code copies them from `context/` by id), and `build` reads nothing else, so
  the same `resume.yaml` always gives the same PDF.
- **Summary and bullets are generated per offer** in one model call, not picked from a fixed list. No
  automated fact checks: the human reads every bullet before sending. `score` never edits the
  resume itself; its notes feed exactly one `tailor` revision (no open-ended loop), and the
  rest is advice for the human.
- **Models via `claude -p`, behind `core/llm.py`.** One function (`complete_json`: prompt +
  JSON schema → structured output), our own system prompt, no tools except WebSearch/WebFetch
  for the cover letter. Moving to the Anthropic
  API (e.g. for Batch at volume) means reimplementing only that function.
- **`core/` vs `flows/` split.** `pipeline/core` must never import an orchestrator. Prefect
  is the first orchestrator; switching to Dagster later means rewriting only `flows/`.
- `tailor` writes experiences ongoing first (`dates` ending in "currently"/"Present"), then
  newest first (by `start`); education newest first; projects most relevant first. `build`
  prints everything in `resume.yaml` order.
- **Degree names follow the job's country**, in code (`resume.ENGINEERING_SYSTEM`): Tunisia
  and France use the engineering-school system (cycle préparatoire + diplôme d'ingénieur),
  elsewhere the bachelor/master equivalents (ESPRIT's diploma is officially equivalent to a
  master's in software engineering). The model only reports `offer.country`; the names
  come from `names` in `context/studies/*.md`.

## Roadmap

1. ✅ Foundation: context/ KB, resume.cls, Jinja renderer, validator, build checks, generic baseline.
2. ⏳ Fill the raw fact dumps (`pipeline check` lists thin files), ingest project repos, port the legacy
   devops/java/frontend/nextjs variants into `offers/`.
3. ⏳ Automation (Prefect, `pipeline/flows/`): fetch offers (RSS / email alerts / pasted URLs;
   trafilatura or Crawl4AI; no scraping of sites whose ToS forbid it) → SQLite dedupe
   (`pipeline/state/`) → cheap fit filter (small model via `llm.py`) → `core.tailor.tailor()`
   → build → score → notify (ntfy/Telegram). A human reviews every
   resume before it is sent; never auto-apply.

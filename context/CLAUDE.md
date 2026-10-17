# context/: the knowledge base

Everything here is **fact about Iheb** and the only material a resume may use. Keep it
exhaustive: it should hold far more than any single resume shows. Edit it only with facts the
user has provided or confirmed (or extracted from their repos via `/ingest-project` and then
reviewed). Run `.venv/bin/python -m pipeline check` after every change; it also lists files
that are still thin.

## Files

| Path | Holds |
|---|---|
| `profile.yaml` | name, `pdf_name`, header `contacts` (`newline: true` starts a 2nd header line), `notes` (free-form, for the agent; no summaries: `tailor` writes one per offer) |
| `skills.yaml` | `categories` → `{id, label, items}`. Any technology a resume names must be here (concepts are written "Concept (Skill, …)") |
| `experiences/<id>.md` | one job/freelance/teaching role |
| `projects/<id>.md` | one side/school project |
| `studies/<id>.md` | one degree |

## Format: YAML frontmatter + raw Markdown body

```markdown
---
id: talan-intern                        # == filename stem
company: Talan
titles: [Software Engineering Intern, Stagiaire ingénieur logiciel]   # first = default; add translations for non-English offers
location: Tunis, TN
start: 2025-02                          # YYYY-MM, used for newest-first ordering
dates: Feb 2025 – Oct 2025              # display string
tags: [ai, data]
stack: [Python, FastAPI]                # full "Technologies used" list
---

## Context
Client, team size, who I reported to, what the product was.

## What I did
- Everything, including small things and things I only touched (say so).

## Numbers
- Only real ones, with where they come from.
```

Projects: `id, name, url, tags, stack, repo` (local path). Studies: `id, school, degrees`
(list, first = default), `start, dates, tags`, and optionally `names: {engineering: {en, fr},
academic: {en, fr}}`: when present, code prints the `engineering` name for jobs in Tunisia or
France and the `academic` (bachelor/master) name elsewhere, in the resume's language.

The **frontmatter** is what code validates and renders. The **body** is never rendered: it is
the raw material resume bullets are written from, and a bullet may only claim what
its own file's body says. So:

- **Write it down, all of it.** Scope, team, tools, problems, decisions, results. Headings and
  lists are free-form; structure it however reads best.
- **Be precise about your part.** "Contributed to", "paired on", "only reviewed" vs "built
  alone", "led". The generated bullet can only claim what the body says.
- **Numbers and technologies** must appear in the body to appear in a bullet, so name them
  where they were actually used.
- `## From past resumes` holds the phrasings from old hand-written resumes (nested items are
  alternative phrasings). They are valid facts; rewrite or expand them freely.
- `TODO` marks missing info to ask the user about; don't fill it with guesses.

Text in a bullet supports `**bold**` and `[label](url)` (the URL must appear in the file);
everything else is escaped for LaTeX automatically, so write plain text (`C#`, `&`, `%` are fine).

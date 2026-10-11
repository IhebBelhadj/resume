---
name: tailor-resume
description: Generate a resume tailored to a job offer. Use when the user pastes a job description, gives a job posting URL or file, or asks for a resume/CV adapted to a role or company.
argument-hint: <job offer text | URL | file path>
---

# Tailor a resume to a job offer

Follow the hard rules in the root CLAUDE.md (no invented facts, select by id, rewrites only reword).

## Steps

1. **Get the offer.** From $ARGUMENTS: pasted text as-is, a URL via WebFetch (ask for the
   text if the page is blocked or behind a login), or a file path. Identify company and role.
2. **Scaffold.** `.venv/bin/python -m pipeline new YYYY-MM-<company>-<role>` (today's date,
   kebab-case). Write the offer into `offers/<slug>/offer.md` (fill the frontmatter).
3. **Analyse the offer** (keep it short): must-haves, nice-to-haves, seniority, domain, and
   10–20 ATS keywords exactly as the offer spells them.
4. **Load context once:** `.venv/bin/python -m pipeline dump`. Do not open the YAML files one
   by one. Open a project repo only if a must-have needs detail the dump lacks; if you learn
   something new there, propose adding it to `context/` (ask first).
5. **Write `offers/<slug>/selection.yaml`** (format: `template/selection.example.yaml`):
   - `offer:` metadata, `keywords:` from step 3, `max_pages: 1` unless told otherwise.
   - `summary:` closest summary id; reword with `{id, text}` only to mirror the offer's
     vocabulary for claims the summary already makes.
   - `skills:` offer-relevant categories and items first; drop irrelevant ones. Rename a
     category `label` if it helps (e.g. "Infrastructure & DevOps").
   - `experiences:` keep every role (no unexplained gaps) but give relevant ones more
     bullets. Pick the `title` variant that fits. Order bullets by relevance, one per
     `variant_of` group. Trim `stack` to what's relevant.
   - `projects:` 2–4 most relevant, most relevant first.
   - `education:` all degrees.
6. **Build:** `.venv/bin/python -m pipeline build offers/<slug>`. If it fails, fix the
   selection (unknown id → check the dump; too many pages → drop the least relevant
   bullets, then projects, then shorten with rewrites) and rebuild until it passes.
7. **Report** to the user, concisely:
   - PDF path and page count
   - must-haves covered → by which bullet/project
   - **gaps**: requirements with no backing in context (suggest what they could add if true)
   - every rewrite (the build prints them) so they can check nothing was overstated
   - keyword coverage and which keywords are missing

---
name: tailor-resume
description: Generate a resume tailored to a job offer. Use when the user pastes a job description, gives a job posting URL or file, or asks for a resume/CV adapted to a role or company.
argument-hint: <job offer text | URL | file path>
---

# Tailor a resume to a job offer

The writing is done by `pipeline tailor` (local `claude -p` calls). Your job
here is to get the offer in, run it, and handle what it can't: gaps and failed builds.
Follow the hard rules in the root CLAUDE.md.

## Steps

1. **Get the offer.** From $ARGUMENTS: pasted text as-is, a URL via WebFetch (ask for the
   text if the page is blocked or behind a login), or a file path. Identify company and role.
2. **Scaffold.** `.venv/bin/python -m pipeline new YYYY-MM-<company>-<role>` (today's date,
   kebab-case). Write the full offer text into `offers/<slug>/offer.md` (fill the frontmatter).
3. **Tailor:** `.venv/bin/python -m pipeline tailor offers/<slug>` (one or two pages by content,
   `--max-pages N` to change the ceiling; the resume is written in the offer's language;
   run in the background, it takes a few minutes). One model call
   writes `resume.yaml` from `context/` + the offer, it is built into the PDF, then a second
   model call scores it into `score.md`.
4. **If it fails:** unknown ids/skills → re-run tailor. Over the page budget → drop or shorten
   bullets in `resume.yaml` (never add facts), `pipeline build offers/<slug>`, then
   `pipeline score offers/<slug>`. A `model error` usually means Claude Code needs `/login`.
5. **Report** to the user, concisely:
   - PDF path and page count, and the score with its top weaknesses (from `score.md`)
   - must-haves covered → by which bullet/project (read `resume.yaml`)
   - **gaps** printed by `tailor`: ask whether they have done those things. If yes, add their
     answer to the right `context/` file body (with their confirmation), then re-run step 3
6. **Cover letter**, if the user wants one: `.venv/bin/python -m pipeline cover-letter
   offers/<slug>` (background; it searches the web). Tell them to check `company.md`, the
   facts the letter cites about the company, before sending.

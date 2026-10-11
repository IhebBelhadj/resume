---
name: ingest-project
description: Turn a local project repository into a context/projects/<id>.yaml entry (or enrich an experience file) so resumes can use it without re-reading the repo. Use when the user points at a project directory or asks to add a project to the resume context.
argument-hint: <path to project repo> [experience id if it belongs to a job]
---

# Ingest a project into context/

Goal: read the repo **once**, cheaply, and leave a reviewed, compact context file so future
tailoring never needs to open the repo again.

## Steps

1. **Check access.** The path must be readable; if it isn't, tell the user to add it to
   `permissions.additionalDirectories` in `.claude/settings.json` (or start with `--add-dir`).
2. **Skim, don't crawl** (cap ~15 file reads):
   - README / docs, package manifests (`package.json`, `pyproject.toml`, `pom.xml`,
     `docker-compose.yml`, CI workflows, IaC), top-level directory layout.
   - `git -C <path> log --oneline | wc -l`, first/last commit dates, and
     `git -C <path> shortlog -sn` to judge the user's share of the work.
   - Only open source files to confirm a claim (e.g. "uses WebSockets").
3. **Draft** `context/projects/<id>.yaml` following `context/CLAUDE.md` (or new bullets for
   `context/experiences/<id>.yaml` if it's work done in a job): name, url (ask if unknown),
   `repo: <path>`, tags, stack, 3–6 bullets with ids, notes. Bullets describe what exists
   in the repo; **no metrics unless the repo or the user provides them**.
4. **Ask the user** to confirm: their role/ownership, team size, impact or metrics, public
   URL, and whether anything is confidential. Mark unknowns as `TODO` in `notes`.
5. Save, then run `.venv/bin/python -m pipeline check`.

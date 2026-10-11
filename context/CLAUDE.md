# context/: the knowledge base

Everything here is **fact about Iheb** and the only material a resume may use. Keep it
exhaustive: it should hold more than any single resume shows. Edit it only with facts the
user has provided or confirmed (or extracted from their repos via `/ingest-project` and then
reviewed). Run `.venv/bin/python -m pipeline check` after every change.

## Files

| Path | Holds |
|---|---|
| `profile.yaml` | name, `pdf_name`, header `contacts` (`newline: true` starts a 2nd header line), `summaries` (id/tags/text), `notes` |
| `skills.yaml` | `categories` → `{id, label, items}`. Any skill a resume lists must be here |
| `experiences/<id>.yaml` | one job/freelance/teaching role |
| `projects/<id>.yaml` | one side/school project |
| `studies/<id>.yaml` | one degree |

## Schema

```yaml
# experiences/<id>.yaml   (filename stem == id)
id: talan-intern
company: Talan
titles: [Software Engineering Intern]   # first = default; selection may pick another (e.g. role-flavoured)
location: Tunis, TN
start: 2025-02                          # YYYY-MM, used for newest-first ordering
dates: Feb 2025 – Oct 2025              # display string
tags: [ai, data]
stack: [Python, FastAPI]                # full "Technologies used" list
bullets:
  - id: ti-keycloak                     # globally unique; prefix with an owner abbreviation
    tags: [security, iam]
    text: Secured the platform with Keycloak IAM ...
  - id: ti-keycloak-nginx
    variant_of: ti-keycloak             # alternative phrasing of the same fact (same file only)
    text: ...
notes: |                                 # never rendered; context for the agent (clients, team size, caveats)

# projects/<id>.yaml: id, name, url, tags, stack, repo (local path), bullets, notes
# studies/<id>.yaml:  id, school, degrees (list, first = default), start, dates, tags, bullets, notes
```

Text supports `**bold**` and `[label](url)`; everything else is escaped for LaTeX
automatically, so write plain text (`C#`, `&`, `%` are fine).

## Writing good bullets

- One fact per bullet, with impact or numbers when real (Lighthouse scores, "30+ members").
- Prefer adding a **new variant** (`variant_of`) over editing a bullet into something
  offer-specific; keep the original phrasing available.
- Tag generously (`backend`, `devops`, `data`, `ai`, `frontend`, tech names). Tags are what
  the tailoring agent matches against the offer.
- `TODO` in `notes` marks missing info to ask the user about; don't fill it with guesses.

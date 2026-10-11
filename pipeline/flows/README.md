# flows/

Orchestration wrappers ONLY (Prefect). Each task here is a thin call into `pipeline/core/`.
No business logic, prompts, or parsing in this folder — so swapping Prefect for Dagster
means rewriting only this folder. Not implemented yet (see roadmap in /CLAUDE.md).

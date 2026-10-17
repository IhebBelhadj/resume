---
id: talan-data-consultant
company: Talan
titles: [Data engineering Consultant, Data Engineering Consultant]
location: Tunis, TN
start: 2025-10
dates: Oct 2025 – currently
tags: [data, dbt, snowflake, airflow, ai, consulting]
stack: [Python, FastAPI, React, LangGraph, Redis, dbt, Docker, Informatica, VTOM, Oracle DB, Snowflake, Airflow, Jinja, SQL, XML]
---

<!-- Raw facts: never rendered. Resume bullets are generated from this text per offer and
     must quote it as their source, so write everything down (scope, team, tools, numbers,
     what you only touched). Keep it true; vague is fine, inflated is not. -->

## From past resumes

- Lead the migration of a CRM data integration project to dbt and snowflake
- Developed a native tool in snowflake for writing xml ingestion code based on a given xsd schema and a defined config by the end user, eliminating the need for external ingestion tools
- Working closely with GRDF to fix detected production anomalies in their legacy data pipelines.
- Contributing to the development of an agentic AI system to automate the migration of Informatica mappings to dbt models, drastically reducing conversion time.

## XML ingestion tool on Snowflake (Informatica XML workflows → Snowflake SQL)

My part: I helped Talan create this tool.

- Problem: workflows being migrated rely on old CRM and ERP tools that talk SOAP, so the data
  arrives as XML. Snowflake only offers basic native XML parsing, and the mapping logic lived
  inside Informatica.
- What the tool does: it takes the XML mappings embedded in Informatica's exported XML
  workflows and uses them to generate the matching XML parsing code in Snowflake SQL.
- It turns Snowflake's basic native XML parsing into robust parsing mappings with more than
  100 columns per model, with lineage, an imposed XML schema and input validations:
  basically all an ingestion tool would offer for XML parsing, but natively on Snowflake,
  so no external ingestion tool is needed.
- Written in Python; runs in Snowflake's native Python environment.
  TODO: confirm whether this is Snowpark / Python stored procedures / a Snowflake Native App.
- Users: the developers migrating the XML-based workflows from Informatica to Snowflake.
- TODO: numbers (models/workflows migrated with it, time saved per mapping, team size).

## Custom Airflow library and multi-environment orchestration

My part: I led the architecture and development of the multi-environment data pipeline
orchestration on Airflow, and created a custom library on top of Airflow that gives DAG
developers everything they need, so DAG code stays clean and reads as declaratively as possible.

- Config builder: parses the configuration at runtime. It is source-agnostic through the
  strategy pattern: the config can come from metadata tables on Snowflake, from a dedicated
  database instance holding metadata, or from JSON variables in Airflow.
- Runtime params: the formatting and mapping needed to manipulate Jinja templating for params
  defined at runtime are abstracted away in utils, so DAG authors don't write that plumbing.
- Dry run: lets a data workflow keep running while some parts of the pipeline are under
  maintenance.
- Downstream event propagation: orchestrated how events propagate downstream to control
  which DAGs get triggered.
- Event-driven, asset-based DAG orchestration: formalized it in the library so implementation
  details are hidden from DAG developers.
- State store: push and fetch state between DAGs, so variable state propagates from one DAG
  to another, with override hierarchy policies deciding which value wins.
- Multi-environment: the orchestration runs across several environments.
  TODO: which environments (dev/rec/prod?), Airflow version and hosting (MWAA, Astronomer,
  self-hosted?), number of DAGs or teams using the library.

## Notes

Client mentioned: GRDF. Scheduler: VTOM.

---
id: talan-intern
company: Talan
titles: [Software Engineering Intern]
location: Tunis, TN
start: 2025-02
dates: Feb 2025 – Oct 2025
tags: [ai, agents, data, backend, fullstack, devops]
stack:
  [
    Python,
    FastAPI,
    Next.js,
    LangGraph,
    LangChain,
    Redis,
    MinIO,
    Airflow,
    Airbyte,
    dbt,
    PostgreSQL,
    Keycloak,
    Docker,
    Nginx,
    Cosmos,
    Bash,
    Docker Compose,
  ]
---

<!-- Raw facts: never rendered. Resume bullets are generated from this text per offer and
     must quote it as their source, so write everything down (scope, team, tools, numbers,
     what you only touched). Keep it true; vague is fine, inflated is not. -->

## Context

- 6-month internship (end-of-studies), Feb 2025 – Oct 2025. TODO: team size, who I reported to.
- The application is called Horizon. Its purpose: dynamic chart generation (a multi-agent system turns
  questions into SQL and charts), with CDC so charts update in real time.
- Horizon is hosted locally, on purpose: the idea is a local data system with minimal cost, avoiding
  cloud costs by running your own data platform. Airbyte, dbt and Airflow all run locally.

## Self-hosted infrastructure (what I worked on)

- Running Airbyte, Airflow and dbt locally needs a way to orchestrate and connect the instances; I used
  Nginx as the gateway in front of them.
- Worked on connecting the instances through TLS, with certificate sharing between them.
- Worked on the provisioning through shell scripts and per-instance Docker Compose files with shared
  Docker network definitions. In effect I rebuilt by hand what Kubernetes gives by default (service
  networking, provisioning, gateway/ingress, TLS between services).
- Hosted the dbt projects in Airflow with Cosmos (astronomer-cosmos).
- Designed to run inside a LAN: an exposed IAM solution (Keycloak) authenticates every service, and the
  whole instance is hidden behind a VPN. TODO: which VPN.

## From past resumes

- Integrated a multi-agent system with LangGraph for dynamic SQL and chart generation, enabling no-code data exploration.
- Built a real-time CDC pipeline refreshing charts live, enabling instant monitoring through the AI first client interface.
  - Built a real-time CDC pipeline refreshing charts live, enabling instant monitoring.
- Developed an end-to-end data pipeline with MinIO, Nessie, Airflow, and dbt to manage ingestion, transformation, and ML forecasting.
  - Developed an end-to-end data pipeline with MinIO, Airflow, Airbyte, and dbt to manage ingestion, transformation, and ML forecasting.
  - Developed an end-to-end data pipeline with MinIO, Delta Lake, Airflow, and dbt to manage ingestion, transformation, and ML forecasting.
  - Built and deployed an end-to-end data pipeline with Airflow and dbt on Dockerized infrastructure, ensuring reproducible workflows and enabling easy scaling of replicas under load.
- Secured the platform with Keycloak IAM using role- and group-based access control.
  - Secured the platform with Keycloak IAM using role- and group-based access control, and built an Nginx gateway to secure the private services network.
- Implemented a caching system through Redis reducing network I/O calls for the agentic system for context retrieval.
- Automated deployments via GitHub webhooks and Bash scripts on a Docker Compose cluster, improving release consistency.
- Built a Next.js frontend leveraging WebSockets to deliver instant feedback and live chart updates for a seamless user experience.
- Optimized frontend performance with persisted state to reduce network calls and enable offline viewing, and implemented optimistic updates for a faster, more responsive user experience.

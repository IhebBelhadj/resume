# Resume score: 4.5/10

_2026-10-19-oneleet-fullstack, scored by claude-opus-5-5_

Likely reject, at most a long-shot maybe. Your TypeScript/React full-stack evidence is solid and specific. The K-Rose bullets on server-side pagination, indexed queries, audit logs and Axiom/Sentry monitoring match several of the listed responsibilities almost word for word. But the offer is built around Go, and Go appears nowhere on your resume. The offer also asks for 5+ years of full-stack experience, and your dates show about 3 (Aug 2023 – present), with part of that as an intern and part-time freelance work. Your current main role, which is the first thing a screener reads, is Python/Airflow/Snowflake data engineering rather than full-stack product work. Missing two hard must-haves puts you in "adjacent profile" territory, however strong the TypeScript side is.

## Weaknesses

- No Go anywhere on the resume. The role says 'Working primarily in Go' and the qualifications ask for 'expertise in Go'. Your backend languages are TypeScript/Node.js and Python, so the core backend must-have is missing.
- Experience falls short of '5+ years of fullstack software development'. Your earliest professional entry is Nexits, Aug 2023, so you have about 3 years. That includes an 8-month internship (Talan, Feb–Oct 2025) and part-time freelance work (K-Rose), so the full-time full-stack equivalent is lower still.
- Your first role is not a full-stack role. 'Software Engineer, Talan, Oct 2025 – Present' is Python, Airflow, Snowflake, dbt and Informatica migration. A screener reading top-down sees a data engineer first, and your strongest full-stack evidence (K-Rose) only comes second.
- No evidence of working directly with customers or turning user feedback into changes. The offer stresses this twice (responsibilities and qualifications). K-Rose says the portal 'replaces email, phone and spreadsheet workflows' but never says you gathered requirements from or iterated with the client.
- No gRPC. You only show REST (OpenAPI) and tRPC.
- Third-party integration and upstream-failure handling are shown only in a side project (Playpex: TMDB, subtitle providers, JSON 502). There is no professional bullet integrating external services.
- Few outcome metrics for full-stack work. K-Rose and Nexits bullets describe what you built (pagination, historization, components) but give no users, volume, latency or adoption numbers. 'improving load times and UX' gives no figure.
- Caching is listed in skills (Redis, Upstash Redis), but no bullet shows you caching anything, even though the offer explicitly asks for 'caching, pagination, and query design for high-volume data'.
- No feature-usage analytics (usage, success rates, engagement). Your monitoring evidence covers errors and logs, not product analytics.
- The skills section carries offer-irrelevant weight (Snowflake, dbt, Payload CMS, Terraform, Python-heavy items) and is long. For this role it dilutes the TypeScript/React signal.

## Strengths

- Strong, concrete TypeScript/React/Next.js full-stack evidence at K-Rose: you built a live B2B portal and back office (linked kairouanrose.com) end to end.
- Bullets map directly onto the offer's responsibilities: server-side pagination, sorting, filtering and debounced search backed by btree/partial indexes (query design for high-volume data), and the delivery calendar from one filtered query per month (mapping complex backend data to actionable UI).
- Production monitoring and observability are clearly evidenced: structured logging to Axiom, and Sentry on client and server.
- Data transformation between system formats is clearly met: the Talan tool maps Informatica XML workflows to Snowflake SQL, with schema enforcement and lineage, and was used to migrate 20+ workflows and 100+ models.
- Covers two bonus items with evidence: workflow orchestration (Airflow, 850+ DAGs, event-driven triggering) and real-time data visualization (WebSocket live charts, React admin dashboard).
- Security-adjacent work fits a security/compliance product: append-only audit log with field-level diffs, server-side access rules, Keycloak RBAC, CMS hardening (exposed route removed, brute-force lockout, GitHub OIDC with least-privilege IAM).
- Error handling for upstream failures is shown explicitly (Playpex: uniform error codes, JSON 502 so the UI never hangs).
- The summary is focused and uses the offer's language ('turning complex data into clear interfaces', 'efficient queries', 'observable production systems').

## Requirements

| | Requirement | Evidence in the resume |
|---|---|---|
| ❌ | 5+ years of fullstack software development experience | Earliest entry: Full-stack Developer, Nexits, Aug 2023 – Sep 2024 (~3 years total, including internship and part-time freelance work) |
| ❌ | Expertise in Go | — |
| ✅ | Expertise in JavaScript/TypeScript | Languages: TypeScript, JavaScript; K-Rose: 'Next.js, React, TypeScript, Payload CMS'; Nexits: Next.js, tRPC, TypeScript |
| ⚠️ | Strong experience building production APIs (REST and/or gRPC) | Playpex: 'Designed a versioned REST API (OpenAPI 3.1, spec-first...)' (side project); Nexits: tRPC migration; K-Rose API routes. No gRPC, and no professional REST API design bullet |
| ⚠️ | Integrating with third-party services | Playpex: 'integrating third-party sources (TMDB, subtitle providers)' (side project only) |
| ✅ | Building responsive, intuitive UIs with modern JS frameworks (React preferred) | K-Rose client portal and back office; 'Built reusable frontend components and a hybrid state management system (route-based state and Zustand)' |
| ✅ | Data transformation and mapping between different system formats | 'maps Informatica XML workflows to Snowflake SQL parsing code with schema enforcement, lineage and input validation' |
| ⚠️ | Asynchronous programming patterns and API optimization techniques | 'background jobs, retries, dead-letter queues and cron schedules with pg-boss' (with the team); server-side pagination and debounced search at K-Rose |
| ⚠️ | Solid debugging skills across the full stack | 'Sentry error tracking on client and server'; no bullet describes a debugging case |
| ✅ | Production monitoring, logging and observability tools | 'structured logging to Axiom in Server Actions and API routes and Sentry error tracking on client and server' |
| ❌ | Gathering requirements from users and translating feedback into improvements | — |
| ❌ | Strong communication skills and comfort working directly with customers | Only 'English (C1)'; no customer-facing work stated |
| ⚠️ | Balance technical excellence with shipping immediate value | K-Rose platform shipped and live; 'Hardened the CMS before launch' |
| ⚠️ | Robust error handling / fallback for upstream service failures | Playpex: 'upstream failures return a JSON 502 so the UI never hangs' (side project) |
| ⚠️ | Caching, pagination and query design for high-volume data | Pagination and indexes at K-Rose; caching only listed in skills (Redis, Upstash Redis) |
| ❌ | Feature usage analytics (usage, success rates, engagement) | — |
| ⚠️ | Bonus: background in cybersecurity or security tools | Audit log, Keycloak RBAC, CMS hardening, GitHub OIDC least-privilege IAM; no security-product role |
| ✅ | Bonus: data visualization components | 'Next.js frontend using WebSockets for live chart updates'; delivery calendar daily load map |
| ✅ | Bonus: workflow engines and async job orchestration | 'multi-environment async workflow orchestration on Airflow (850+ DAGs)'; pg-boss job queues |

## To raise the score

- **high** · gap to close: Learn Go and ship something real with it (e.g. port the Playpex REST API, or build a small Go service with a React front end, published on GitHub). Without Go you fail the role's primary language requirement.
- **high** · add to context/ if true: If you have written any Go, even in a side project or at work, add it with a concrete bullet. It is the single most damaging absence.
- **high** · add to context/ if true: If you worked directly with the K-Rose client (or Nexits users) to gather requirements and change features based on their feedback, add a bullet saying what feedback led to what change.
- **medium** · resume edit: Lead with full-stack work. Shorten the Talan Software Engineer entry to its data-mapping and orchestration angle, and put K-Rose's 'end-to-end' framing in the summary with the live URL, so the first third reads as full-stack product engineering, not data engineering.
- **medium** · add to context/ if true: If you implemented caching (Redis/Upstash) in any shipped feature, add a bullet saying what was cached and the effect; right now it is only a skill tag.
- **medium** · add to context/ if true: If you integrated third-party services professionally (payments, email, Clerk webhooks, external APIs) or handled upstream failures at work, add it, so that evidence isn't limited to Playpex.
- **medium** · add to context/ if true: If you have usage or outcome numbers (number of clients or orders on K-Rose, load-time gains at Nexits, Vercel Analytics usage tracking), add them to the relevant bullets.
- **low** · resume edit: Trim the skills section: drop or merge Snowflake, dbt, Payload CMS and Terraform, and keep the TypeScript/React/API/observability items the offer asks for.
- **low** · resume edit: Reword 'improving load times and UX' (Nexits) to something concrete, or cut the vague outcome rather than leave it unquantified.
- **low** · add to context/ if true: If you have used gRPC or Protocol Buffers anywhere, add it.

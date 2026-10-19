# Resume score: 6.5/10

_2026-10-kapa-fullstack, scored by claude-opus-5-5_

Borderline shortlist. Your agentic RAG work (ChromaDB, Sentence Transformers, an LLM relevance-grading sub-agent, a LangGraph text-to-SQL agent) and your React/Next.js work are close to what Kapa builds, and few applicants will have both. The evidence for the role's main focus is thin, though. No bullet describes a Python backend service you built: FastAPI appears only in a stack line. The RAG system was an internship project with no users, volume, latency or quality numbers, while Kapa answers thousands of questions a day. Your "3+ years" adds up to about 3 years 2 months only if the internship and a 3-month freelance gig count. And your current role, the first thing a reader sees, is mostly data engineering (Informatica→dbt, Snowflake, Airflow) rather than RAG or full-stack. I would put you in the "maybe" pile, leaning yes because of the RAG match. I would not call immediately.

## Weaknesses

- No Python backend evidence. The role is mostly Python (RAG engine, analytics, integrations, data connectors), but no bullet says you built a Python API or service. FastAPI and Flask appear only in the skills and stack lists. Your Python bullets are a Snowflake codegen tool, an Airflow library and agent logic, not web backends.
- Your RAG work has no production scale. The 'agentic RAG system for a text-to-SQL LLM agent' was built during the Talan internship and has no users, query volume, latency or retrieval-quality figures. Kapa's pitch is serving thousands of questions per day, and nothing on your resume shows you have run RAG under load.
- Your best match is buried. The current Talan role at the top leads with Informatica→dbt conversion, a Snowflake XML tool and 850+ Airflow DAGs, which reads as data engineering. The Horizon RAG bullets only appear in the third entry, below K-Rose.
- Your years are borderline. From Aug 2023 to now is about 3 years 2 months, and that total includes an 8-month internship (Feb–Oct 2025) and a 3-month freelance gig. A strict reader will count about 2 years of full-time non-intern experience.
- Several bullets are vague or weak on ownership: 'Contributing to an agentic AI system… drastically reducing conversion time' has no number and no stated part for you; 'Integrated a LangGraph multi-agent system'; 'contributed to migrating'; 'Worked with the team on the AWS deployment'. The verbs don't say what you personally built.
- Nothing shows SDK or library maintenance for external developers. 'Maintain our React SDK' is a listed duty, and the closest you have is Playpex's shared protocol package in a personal project.
- Nothing shows ML, deep learning or NLP beyond calling LLMs and using embeddings: no evaluation, fine-tuning or retrieval-quality work.
- 'Freelance Job' at Nexits is a placeholder title and looks careless.
- The role is in the Netherlands (remote). Your only phone number is Tunisian (+216), and the resume says nothing about where you are based or whether you can work for an NL/EU employer. A screener will worry about that.
- Some of the space goes to less relevant material: the Data skills line (Airflow, dbt, Airbyte, Snowflake), Angular, and the K-Rose order state machine and audit-log bullet. That space could go to Python and RAG detail.

## Strengths

- Your agentic RAG experience is a direct domain match: 'agentic RAG… ChromaDB with Sentence Transformers embeddings' plus an 'LLM relevance-grading sub-agent (Corrective RAG)'. That is Kapa's core product area.
- You have shipped real React frontends: the K-Rose client portal (order wizard with Zod, SWR optimistic updates), the Playpex React dashboard with TanStack Query and WebSockets, and a Next.js frontend with live chart updates.
- You have worked across the stack and the infrastructure: Terraform, Docker Compose and GitHub Actions zero-downtime deploys on AWS at Nexits; Redis caching for agent context retrieval.
- Your Talan bullets have concrete numbers: '20+ workflows and 100+ models', '850+ DAGs', a 100 Lighthouse score at Nexits.
- Your startup and solo work suits a small, loosely defined environment: 'In a small startup team', 'Built alone' (twice), the freelance lead role at K-Rose.
- The summary leads with the right keywords (LLM agents, RAG, Python, React), and the key terms are bolded, so the resume is quick to skim.
- Your Master's in Software Engineering meets the degree requirement.

## Requirements

| | Requirement | Evidence in the resume |
|---|---|---|
| ✅ | Degree in CS, ML, mathematics, statistics or related field | Master's in Software Engineering, ESPRIT, Sep 2022 – Sep 2025 |
| ⚠️ | 3+ years of software engineering experience | Nexits Aug 2023 – Sep 2024; Nexits freelance Nov 2024 – Feb 2025; Talan intern Feb 2025 – Oct 2025; Talan Oct 2025 – Present (about 3.2 years, including an internship) |
| ⚠️ | Complex systems in both backend and frontend | Frontend is strong (K-Rose React portal, Next.js with WebSockets). Backend evidence is a PostgreSQL state machine and audit log, plus 'migrating the SaaS to Next.js, tRPC'. No Python backend service is described. |
| ⚠️ | Affinity for ML, deep learning (incl. LLMs) and NLP | 'Built an agentic RAG system for a text-to-SQL LLM agent… ChromaDB with Sentence Transformers embeddings'; 'LLM relevance-grading sub-agent'. LLMs are well covered; nothing on ML/DL or NLP modelling. |
| ⚠️ | Effective in a fast, loosely defined environment | 'In a small startup team, contributed to migrating the SaaS…'; 'Built alone a Python tool…'; Lead Full-stack Engineer (Freelance) |
| ⚠️ | Scale Python RAG engine infrastructure | 'Built an agentic RAG system…'; 'Implemented a Redis caching layer that reduces network I/O for the agents' context retrieval'. No scale or production evidence. |
| ⚠️ | Analytics platform features (React + Python) | 'Integrated a LangGraph multi-agent system that turns user questions into SQL and charts'; 'Next.js frontend with WebSockets for live chart updates' |
| ❌ | Client integrations to deploy for customers (React + Python) | — |
| ⚠️ | Give the product access to new kinds of data (Python) | 'Built alone a Python tool running natively in Snowflake that generates XML parsing code'; Data skills: Airbyte, Airflow |
| ❌ | Maintain a React SDK | Closest: 'dependency-free protocol package shared by every client, checked by contract tests' (Playpex, personal project) |

## To raise the score

- **high** · add to context/ if true: If you built or exposed a Python API (FastAPI endpoints, a WebSocket server, the agent-serving layer for Horizon), add a bullet that names the endpoints, how it was deployed and who used it. This is the biggest gap for a role that is mostly Python.
- **high** · add to context/ if true: If the Horizon RAG system had real users or was evaluated, add the figures: queries per day, latency, retrieval precision or answer accuracy before and after relevance grading. Scale and quality numbers are what Kapa cares about.
- **medium** · resume edit: Move the RAG material up. Put the agentic RAG and relevance-grading story in the summary as a concrete claim (for example, 'built a Corrective RAG pipeline on ChromaDB'), and in the current Talan role lead with the agentic AI bullet. Readers should see RAG before Snowflake, dbt or Airflow.
- **medium** · add to context/ if true: If you have done SDK or library work for third-party developers (a published npm package, embeddable widget, public API client), add it. Kapa's React SDK and customer integrations have no evidence on your resume.
- **medium** · add to context/ if true: State your part and the result in the Informatica→dbt agentic system. Replace 'Contributing to… drastically reducing conversion time' with what you built and a measured gain, if you have one.
- **medium** · add to context/ if true: If you can work in the Netherlands or EU, or are open to relocating, add your location and work status to the header. Remote in the NL usually requires it.
- **medium** · gap to close: Build a small public project on retrieval evaluation or NLP (for example, a RAG eval harness over documentation with measured recall and answer quality, served by a FastAPI backend with a React widget). It would cover the ML/NLP, Python backend and SDK gaps at once.
- **low** · resume edit: Rename 'Freelance Job' to the real role (for example, 'Freelance Full-stack Developer') and replace 'Integrated', 'contributed to' and 'Worked with the team on' with what you specifically did, where the facts support it.
- **low** · resume edit: Cut or shrink what Kapa doesn't use: the Data skills line, Angular, and the K-Rose state machine and audit-log bullet. Use the space for Python and RAG detail.

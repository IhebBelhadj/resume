# Resume score: 5.4/10

_2026-10-kapa-fullstack, scored by claude-opus-5-5_

Maybe, leaning no. Iheb has real React/Next.js and Python experience, and he has hands-on LLM agent work (LangGraph multi-agent SQL/chart generation, agentic Informatica-to-dbt migration). That fits Kapa's "affinity for LLMs" line. But the resume never mentions RAG, retrieval, embeddings or vector search, and that is the core of Kapa's product. It shows no SDK or library he maintained, no customer-facing integration or embeddable widget, and no scale numbers for any system. The "3+ years" only adds up if you count a 13-month role, an 8-month internship and a freelance job that overlaps his current consultancy, all while he was studying for his Master's until Sep 2025. The role is listed as Mid-Senior in the Netherlands, and the resume shows a Tunis base with no word on work authorization or relocation. I'd keep him in the pile behind candidates with production RAG experience, but I wouldn't call first.

## Weaknesses

- The resume never mentions RAG, retrieval, embeddings, vector databases or search quality. Kapa's main backend work is 'Scale the infrastructure that powers the Kapa RAG engine', and the closest thing on the page is 'a LangChain agent that answers questions about my experience' on a personal portfolio.
- Nothing shows systems at scale. Kapa answers 'thousands of developer questions per day', and no bullet gives traffic, latency, data volume, user counts or uptime. The only numbers are commit counts (~140 of 164) and a Lighthouse score of 100.
- The seniority case is weak. Professional time is Nexits (Aug 2023–Sep 2024, 13 months), a Talan internship (Feb–Oct 2025), the Talan consultancy (Oct 2025–now) and K-Rose freelance (Feb–May 2026), which overlaps the consultancy. The Master's ran until Sep 2025, so most of that time was alongside study. For a Mid-Senior role, '3+ years' looks borderline.
- No React SDK, published package or embeddable client integration appears anywhere. 'Maintain our React SDK' and 'client integrations… to deploy Kapa for our customers' are both uncovered.
- Location and work authorization are missing. The role is in the Netherlands and every location on the resume is Tunis, TN or remote, with no line on relocation, visa or EU authorization. Many screeners filter on this before reading anything else.
- The current role (Talan consultant) is about Informatica, Snowflake, dbt and Airflow migration work. That is enterprise data engineering, not product engineering, so the most recent full-time role is the least relevant one.
- Several bullets are vague or hedged: 'drastically reducing conversion time' (no number), 'optimizing load times' (no number), 'Contributing to', 'Helped build', 'Integrated a LangGraph multi-agent system' (it's unclear what he personally built).
- The summary is generic ('backend systems, data pipelines, and agentic AI… cloud-native… scalable infrastructure') and doesn't connect him to LLM-powered developer products. The skills list includes Kafka, Spark, Kubernetes and Terraform, which no bullet backs up.

## Strengths

- He has worked on both stacks Kapa uses. React/Next.js/TypeScript runs through K-Rose, Nexits and the Talan internship, and Python/FastAPI shows up in the Talan internship and consultancy.
- He has real LLM agent work: 'Integrated a LangGraph multi-agent system for dynamic SQL and chart generation, enabling no-code data exploration' plus the agentic Informatica-to-dbt migration system. That covers the LLM affinity requirement.
- The Talan internship is close to Kapa's analytics platform: an LLM backend plus a 'Next.js frontend using WebSockets for instant feedback and live chart updates' is AI-driven analytics in React and Python.
- The K-Rose role shows he can own a project end to end: led architecture, wrote ~140 of 164 commits, reviewed and merged the team's PRs, built an order state machine with role-based transition matrices and server-side data isolation. That suggests he can work with a small founding team.
- The portfolio's LangChain Q&A agent is essentially a small 'Ask AI' assistant, which is Kapa's product.
- He has a relevant degree (Software Engineering Master, ESPRIT), and the resume is one tight page.

## Requirements

| | Requirement | Evidence in the resume |
|---|---|---|
| ✅ | Degree in CS, ML, mathematics, statistics or related field | Software Engineering Master, ESPRIT, Sept 2022 – Sep 2025 |
| ⚠️ | 3+ years of software engineering experience on complex systems, both backend and frontend | Nexits Aug 2023 - Sep 2024; Talan intern Feb 2025 – Oct 2025; Talan consultant Oct 2025 – currently; K-Rose Feb 2026 – May 2026. About 3 years only if you count the internship, the overlapping freelance work and work done during the Master's |
| ⚠️ | Affinity for ML, deep learning (incl. LLMs) and NLP | Integrated a LangGraph multi-agent system for dynamic SQL and chart generation; agentic AI system for Informatica-to-dbt migration. Covers LLMs only; nothing on deep learning or NLP |
| ⚠️ | Work effectively in a fast, loosely defined environment | Led architecture and end-to-end delivery of a B2B ordering platform (freelance). Implied, not stated |
| ❌ | Scale infrastructure powering a RAG engine (Python) | — |
| ⚠️ | Build features in an analytics platform (React + Python) | LangGraph multi-agent system for dynamic SQL and chart generation, enabling no-code data exploration; Next.js frontend using WebSockets for live chart updates |
| ❌ | Client integrations used to deploy the product for customers (React + Python) | — |
| ⚠️ | Give the system access to new kinds of data (Python) | Python tool running natively in Snowflake that generates XML parsing SQL from Informatica workflow mappings; Airflow pipeline orchestration. This is ETL, not ingestion into an LLM/RAG system |
| ❌ | Maintain a React SDK | — |
| ❌ | Work directly with founding team and research engineers | — |
| ❌ | Location: Netherlands (implied work authorization/relocation) | — |

## To raise the score

- **high** (add to context/ if true): If you have built retrieval in any project (document chunking, embeddings, a vector store such as pgvector/Chroma/Pinecone, reranking, retrieval evaluation), including in the portfolio agent or the Talan LangGraph system, add it to context/ and put it in the bullets with the stack you used.
- **high** (gap to close): Build and ship a small production-style RAG system over real technical docs (ingestion, embeddings, retrieval, eval set, latency/cost numbers) and add it as the lead project. This is the biggest gap against Kapa's core work.
- **high** (add to context/ if true): If you have EU work authorization or are willing to relocate to the Netherlands, say so in the contacts line or the summary.
- **medium** (add to context/ if true): If any of the systems you built had real usage (users, queries per day, orders processed, data volumes, latency, how much the dbt migration cut conversion time), add those numbers to the existing bullets in place of 'drastically' and 'optimizing load times'.
- **medium** (edit the resume (facts it already has)): Rewrite the summary for this role: a full-stack Python + React engineer who builds LLM-powered products (multi-agent SQL/chart assistant, Q&A agent). Drop the 'cloud-native / scalable infrastructure' boilerplate.
- **medium** (edit the resume (facts it already has)): Reword the portfolio bullet so it reads as an embedded 'Ask AI' assistant that answers questions over your own content (only as far as context/ supports it), and consider moving it up, since it is the closest thing to Kapa's product.
- **medium** (add to context/ if true): If you have published an npm package, an embeddable widget or a reusable component library (the Nexits reusable components may count), add it; it maps directly to 'Maintain our React SDK' and client integrations.
- **low** (edit the resume (facts it already has)): Cut skills no bullet backs up (Kafka, Spark, Kubernetes, Terraform, MongoDB) unless context/ shows real use, and use the space for detail on the Python/FastAPI backend side of the Talan internship.
- **low** (edit the resume (facts it already has)): Replace hedged verbs where context/ supports more direct ownership ('Contributing to', 'Helped build', 'Integrated'), and state your own part in the agentic migration system.

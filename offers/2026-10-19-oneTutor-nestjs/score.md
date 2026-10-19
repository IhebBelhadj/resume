# Resume score: 7.6/10

_2026-10-19-oneTutor-nestjs, scored by claude-opus-5-5_

I would shortlist you. The one hard requirement is solid React + TypeScript, and your resume shows it clearly: about three years across K-Rose, both Nexits roles and Playpex, with concrete work like an order wizard, a TanStack Table view, a shared component library and a Next.js/tRPC migration. You also cover most of the nice-to-haves well, including RAG, embeddings, ChromaDB and LangChain/LangGraph. Three things keep this out of the call-immediately range. First, nothing on the page says you can work on-site in Munich: you have a Tunisian phone number, every role is in Tunis or remote, and the only signal is "Open to relocation", with no mention of work authorization or a visa. Second, there are no outcome metrics anywhere. Third, your AI work is in Python while the role builds AI features in NestJS/TypeScript. A screener at a small startup with more than 100 applicants will notice the relocation and visa question first.

## Weaknesses

- Nothing shows you can start on-site in Munich. The header has a +216 number, every job is in Tunis or remote for Paris, and the only hint is "Open to relocation" in the summary. The resume doesn't mention a German work permit, Blue Card eligibility or a start date. For a role that says "do not apply if you want a remote position", that is the first thing a screener will check.
- No numbers anywhere. You don't give K-Rose order volume or user count, how big the Nexits migration was, or any effect from the Redis cache ("cutting network I/O" has no figure). The offer opens with its own impact numbers (35,000+ users), and your bullets say what you built but not what it achieved.
- No NestJS, and the backend evidence comes from Payload CMS hooks, tRPC and Server Actions. Express.js appears only in the skills list and is never used in a bullet. That's acceptable because the offer takes React or NestJS, but it weakens the 'expand into backend' story the offer describes.
- Your AI work (the RAG pipeline and LangGraph agents at Talan) is all in Python. Nothing shows an AI-driven feature built in TypeScript or wired into a React or Node product, apart from the Next.js frontend of the Talan tool.
- Your current role, Talan Software Engineer (Oct 2025 – Present), has one bullet, and it is about Informatica, dbt, Snowflake and Airflow, none of which this role uses. Even so, it is the first thing the reader sees under Experience.
- The title "Freelance Job" (Nexits, Nov 2024 – Feb 2025) reads as unprofessional and undersells strong React and TypeScript work.
- Collaboration is thin. The only teamwork evidence is "delivered through code reviews with the Nexits team". You show no pair programming, no work with product or design people, and nothing on mentoring or communication, which the offer says 'matters most'.
- The skills section is padded with low-signal items (SWR, Zustand, Vite, Sentry, Vercel, SQLite, Payload CMS listed separately). It is long and dilutes the TypeScript, React and AI points.
- No prompt engineering or fine-tuning is mentioned. Your RAG grading sub-agent implies prompt design, but the resume never says it.

## Strengths

- Strong React + TypeScript evidence across several roles: K-Rose (Next.js 15 / React 19 / TS, a three-step order wizard with react-hook-form and Zod, TanStack Table, SWR optimistic updates), Nexits (a shared shadcn/ui component library, a Vue → Next.js/tRPC migration, Zustand) and Playpex (a React 19 dashboard with TanStack Query and WebSocket).
- Real backend and data-modeling depth, not just UI. This matches 'design and build APIs, model data':
- an order and delivery state machine with separate admin and client transition matrices, enforced server-side
- idempotency keys and field whitelisting
- an immutable audit log written in the same transaction
- a spec-first OpenAPI 3.1 API with generated types and contract tests
- Good fit with OneTutor's core product, which is grounded, non-hallucinating answers. Your Talan RAG pipeline uses Sentence Transformers embeddings in ChromaDB, with "an LLM sub-agent grading each retrieved result and discarding irrelevant context", alongside LangGraph multi-agent work.
- Testing and production habits are concrete: test-first development with Vitest unit and integration tests, Playwright end-to-end tests, Sentry, structured Axiom logging, and GitHub Actions CI for lint and typecheck.
- Your bullets are specific and technical, in the form 'what was built, with what'. The summary in the first third makes the React + TypeScript + LLM case directly.
- Ownership signals fit 'one of our first engineering hires': as Lead Full-stack Engineer at K-Rose you built the client portal and back office end to end on a live product (kairouanrose.com).

## Requirements

| | Requirement | Evidence in the resume |
|---|---|---|
| ✅ | Solid experience with React + TypeScript (or NestJS + TypeScript) | K-Rose: "Built the client portal and back office ... in one Next.js 15 / React 19 / TypeScript app"; Nexits: "Built the shared React component library (shadcn/ui, Tailwind CSS) and shared generated TypeScript types" |
| ❌ | NestJS + TypeScript backend (alternative to React) | — |
| ✅ | Backend: design and build APIs, model data | "Modelled orders and deliveries with a status state machine ... enforced server-side in Payload hooks"; Playpex: "Designed a spec-first versioned REST API ... (OpenAPI 3.1, generated TypeScript types, contract tests against the spec)" |
| ⚠️ | Develop AI-driven features (in NestJS/TypeScript) | Talan intern: "Built a RAG pipeline that grounds a text-to-SQL agent ..." (Python stack, not TypeScript) |
| ✅ | Frontend: build React components, integrate with backend, improve UX end-to-end | "Built a three-step React order wizard ... SWR notifications with optimistic updates"; Talan intern: "Built the Next.js frontend with WebSockets for live chart updates" |
| ⚠️ | Design, ship, test and maintain features with product/engineering peers | "Developed test-first with Vitest unit and integration tests and Playwright for end-to-end tests; added Sentry error tracking" (testing is shown; working with product people is not) |
| ⚠️ | Code reviews and pair programming | Nexits: "delivered through code reviews with the Nexits team" (no pair programming) |
| ⚠️ | On-site in Munich (no remote) | Summary: "Open to relocation." (no work authorization or availability stated) |
| ❌ | Curiosity, communication, desire to grow | — |
| ❌ | Employment references attached | — |
| ✅ | Nice to have: AI tooling (LLMs, LangChain, RAG, embeddings, vector DBs) | "RAG pipeline ... (Sentence Transformers embeddings in ChromaDB)"; "Integrated a LangGraph multi-agent system"; skills list LangChain and vector databases |
| ❌ | Nice to have: prompt engineering or fine-tuning | — |
| ⚠️ | Nice to have: lean, agile startup environments | Summary: "used to owning work in small startup teams"; K-Rose freelance lead role (no explicit startup or agile context) |

## To raise the score

- **high** · add to context/ if true: If you have the right to work in Germany, are eligible for an EU Blue Card, or can start on a specific date, add it to the header or summary (e.g. 'Relocating to Munich; available from <date>'). Without it, you may be filtered out before anyone reads the bullets.
- **medium** · add to context/ if true: If you have numbers for K-Rose (orders per month, number of B2B clients, staff hours saved), the Nexits migration (pages or components migrated) or the Redis cache (latency or I/O reduction), add them to the matching bullets.
- **medium** · add to context/ if true: If you wrote or tuned prompts (e.g. the grading prompt for the RAG sub-agent, or the text-to-SQL agent prompts), say so explicitly in the Talan intern bullets. That covers the 'prompt engineering' nice-to-have.
- **medium** · add to context/ if true: If you have paired with other developers, worked directly with product owners or founders on scope, or mentored anyone, add one bullet saying so. The offer weighs communication and collaboration above tech.
- **medium** · gap to close: Build a small NestJS + TypeScript service, ideally one exposing a RAG or LLM feature, and put it on GitHub. That closes both the NestJS gap and the 'AI features in TypeScript' gap.
- **medium** · add to context/ if true: Prepare employment references to attach. The offer says applications without them might not be processed.
- **low** · resume edit: Replace the 'Freelance Job' title with a real one such as 'Freelance Full-stack Developer', if your context supports it.
- **low** · resume edit: Move the Talan intern AI bullets up visually, or lead your current Talan bullet with the LangGraph agentic-AI part, so the first entry under Experience reads as AI engineering rather than a data-warehouse migration.
- **low** · resume edit: Trim the skills section. Drop or merge low-signal items (SWR, Zustand, Vite, SQLite, Sentry, Vercel) so TypeScript, React, Node.js APIs and RAG/LLM stand out. Name Express.js in a bullet if you used it, or remove it.

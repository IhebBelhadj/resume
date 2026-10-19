# Resume score: 3.5/10

_2026-10-19-codify-js-dev, scored by claude-opus-5-5_

I would not shortlist this. Your technical match is good. You have hands-on TypeScript, React, Next.js, Node.js, tRPC, PostgreSQL with an ORM, WebSockets and Playwright, and your security work is concrete and above what most medior candidates show. The problem is the "basisvereisten", which Codifly says it will not respond without. Your resume lists no Dutch at all (Arabic, English C1, French B2), and it does not mention Belgian work authorisation: there is a +216 phone number, every role is in Tunis or remote from Paris, and the only clue is "Open to relocation". The 3-year full-stack JavaScript requirement is also only partly backed up. About 13 months are full-time (Nexits, Aug 2023–Sep 2024). The rest is a 3-month freelance job, an 8-month internship and an 8-month part-time freelance job, and your current main role (Talan) is Python and data work. A screener would stop at the language and work-permit checks before reading your stack.

## Weaknesses

- No Dutch. Fluent Dutch is a stated knockout, and your languages line is 'Arabic (native), English (C1), French (B2)'. Codifly says it does not respond to applications that miss a basic requirement.
- Work authorisation for Belgium (EU/EEA/Swiss citizenship or a valid work permit) is not stated anywhere. A Tunisian phone number, Tunis locations and 'Open to relocation' suggest you need sponsorship, which is a second knockout.
- The 3+ years of professional full-stack JavaScript are thin. Only Nexits Full-stack Developer (Aug 2023–Sep 2024) is clearly full-time JavaScript employment. The rest is 'Freelance Job' (3 months), an internship (8 months) and 'Freelance, part-time' K-Rose. Your current main role at Talan is Python, LangGraph, dbt and Snowflake, not JavaScript.
- Your first entry, Talan Software Engineer (Oct 2025 – Present), is a Python/data migration consulting role. It is the first thing a reader sees under experience, and it argues against a JavaScript profile.
- GraphQL and Apollo show up only weakly. GraphQL is in the skills list but no bullet shows it. Apollo Client appears only in EldSync, an Angular/NgRx project you 'contributed to the frontend of'. That is not React, and it is not professional work. Apollo Server and Koa are missing.
- Testing: Jest is listed in skills but no bullet shows Jest tests, and Mocha & Chai are missing. Vitest and Playwright are backed up only on K-Rose.
- NoSQL: MongoDB appears only in the skills list. Redis is used for rate limiting, not as a primary data store.
- Your summary never says how many years of experience you have and never addresses Belgium, Dutch or a hybrid on-site setup, so the first third doesn't answer the screener's first questions.
- The 'Freelance Job' title is vague and reads as unprofessional next to the other titles.
- Some space goes to things that don't help this offer: Astro.js, Vue.js and Electron in the Frontend skills, Terraform, and Keycloak. They dilute the React/Node story.
- None of the bonus items is backed up: React Native, agile practices, RAG/prompt engineering and n8n are all absent.

## Strengths

- Strong, concrete security evidence that fits Codifly's 'security as a vital aspect': CSRF refusal of cross-origin requests, OAuth 2.0 device flow (RFC 8628), HttpOnly signed cookies, scrypt hashing, DNS-rebinding Host checks, HSTS/CSP, HTTPS via Caddy, closing a route that exposed every user record, and per-client server-side access control.
- K-Rose shows end-to-end ownership with specifics: a Next.js 15 / React 19 / TypeScript app, ~140 of 164 commits, reviewing and merging the team's pull requests, a PostgreSQL + Drizzle ORM data model with versioned migrations, an order state machine, idempotency keys and a transactional audit log.
- The stack lines up closely with the offer: React, Vite, Node.js, Express, tRPC, WebSocket, ORM (Drizzle), PostgreSQL, Playwright, TypeScript, REST/OpenAPI, Docker and AWS each appear in at least one bullet.
- The Playpex project is a good portfolio piece for an interview, which Codifly explicitly asks for. It has a Node/Express REST API with an OpenAPI 3.1 spec and contract tests, WebSockets to a React + Vite dashboard, and Drizzle.
- The bonus items are partly covered with real usage: AWS with Docker Compose on EC2, RDS, GitHub Actions with OIDC, plus LangChain/LangGraph agentic systems and Bash.
- The degree requirement is met: Master's in Software Engineering, ESPRIT, 3 years.
- Bullets are concrete throughout: what you built, with which tools, and often a result (Lighthouse 100/100, zero-downtime deploys, fewer network calls).

## Requirements

| | Requirement | Evidence in the resume |
|---|---|---|
| ✅ | Bachelor's in computer science or master's in computer science (3+ years of study) | Master's in Software Engineering, ESPRIT, Sep 2022 – Sep 2025 |
| ⚠️ | At least 3 years of professional full-stack JavaScript experience | Full-stack Developer, Nexits, Aug 2023 – Sep 2024; Freelance Job, Nexits, Nov 2024 – Feb 2025; Software Engineering Intern, Talan, Feb–Oct 2025; Lead Full-stack Engineer (Freelance, part-time), K-Rose, Dec 2025 – Aug 2026 |
| ⚠️ | Fluent Dutch and very good English | languages: English (C1). No Dutch. |
| ⚠️ | Willing to work both on site and remotely (hybrid) | Summary: 'Open to relocation'; remote roles at Nexits (Paris, FR (Remote)) |
| ❌ | EU/EEA/Swiss citizenship or a valid Belgian work permit | — |
| ⚠️ | Recent frontend tech: React 16.8+ with hooks, Apollo Client, Vite | K-Rose: 'Next.js 15 / React 19 / TypeScript app'; Playpex: 'React + Vite dashboard'; Apollo Client only in EldSync (Angular) |
| ✅ | Backend: Node.js, Express/Koa, tRPC | Nexits: 'Next.js, tRPC'; 'Node.js API and worker in Docker Compose'; Playpex stack: Node.js, Express.js |
| ❌ | GraphQL and Apollo Server | GraphQL listed in Backend skills only; no bullet shows GraphQL or Apollo Server |
| ✅ | WebSockets | Talan intern: 'Next.js frontend using WebSockets for live chart updates'; Playpex: 'WebSocket events streaming live sessions' |
| ⚠️ | ORM, NoSQL databases, PostgreSQL | K-Rose: 'PostgreSQL through Payload CMS and Drizzle ORM with versioned migrations'; Redis rate limiting; MongoDB in skills only |
| ⚠️ | Unit and end-to-end tests (Jest, Mocha & Chai, Playwright) | K-Rose: 'Vitest unit tests ... Playwright for end-to-end tests'; Playpex: 'contract tests'. Jest in skills only; no Mocha/Chai |
| ✅ | Fundamentals: HTTP, REST, JSON, Git, HTML5, CSS3 | Playpex: 'versioned REST API defined by an OpenAPI 3.1 spec'; K-Rose: 'reviewed and merged the team's pull requests'; Tailwind CSS |
| ✅ | Thorough knowledge of modern JavaScript and TypeScript static typing | Summary: 'builds TypeScript web platforms end to end'; TypeScript in every JS role's stack |
| ⚠️ | Security concepts (HTTPS, JWT, OpenSSL, CSRF, XSS, SQL injection, OAuth) | Playpex: 'OAuth 2.0 device authorization ... refusal of cross-origin state-changing requests (CSRF)'; Nexits: 'HSTS/CSP headers, HTTPS via Caddy'. JWT, XSS, SQL injection not named |
| ❌ | Bonus: React Native | — |
| ✅ | Bonus: scripting, AWS, Docker | Nexits: 'Node.js API and worker in Docker Compose on EC2, RDS PostgreSQL ... GitHub Actions CI/CD with OIDC'; Bash in Languages |
| ⚠️ | Bonus: Generative AI (LLM, RAG, LangChain, n8n, prompt engineering) | Talan: 'agentic AI system built with LangGraph'; intern: 'LangGraph multi-agent system turning user questions into SQL and charts'. No RAG or n8n |
| ❌ | Bonus: agile techniques and tools | — |
| ⚠️ | Open to .NET and PHP (e.g. WordPress) | PHP in Languages; no .NET |
| ⚠️ | Independent but also works in a team; client-focused | Talan: 'working with the client's teams to fix production anomalies'; K-Rose: 'reviewed and merged the team's pull requests' |

## To raise the score

- **high** · gap to close: Close the Dutch gap before applying. Codifly's knockout is fluent Dutch. If you don't have at least B2 Dutch, this application will most likely be filtered out no matter what the resume says; target English-speaking roles in Belgium instead.
- **high** · add to context/ if true: If you have EU/EEA/Swiss citizenship, a Belgian work permit or a Single Permit route, say so in the header or summary (e.g. 'EU work authorisation'). Without it, a screener assumes you need sponsorship and stops.
- **high** · add to context/ if true: If you have any Dutch, even basic or currently studying, add it with a level to the languages line.
- **medium** · resume edit: Open the summary with your full-stack JavaScript years and ownership (e.g. 'Full-stack TypeScript engineer, 3 years across React/Next.js and Node.js; led the end-to-end build of a B2B ordering platform'). Add 'open to relocating to Belgium, hybrid' instead of the generic 'Open to relocation'.
- **medium** · resume edit: Cut the Talan Software Engineer (current) entry to a single short line. Consider putting the K-Rose lead role first, since it is also within 'Present'-adjacent dates, so the JavaScript evidence leads.
- **medium** · add to context/ if true: If you have used GraphQL (queries, schema, resolvers, Apollo Server) in any role, add a bullet showing it. Otherwise remove GraphQL from the Backend skills, where it now stands without evidence.
- **low** · add to context/ if true: If you have written Jest tests anywhere, name it in a bullet. Otherwise drop Jest from Testing so the list matches what your bullets show (Vitest, Playwright).
- **low** · add to context/ if true: If you have defended against XSS or SQL injection explicitly (output encoding, parameterised queries via Drizzle, CSP for XSS) or worked with JWTs, name those terms in the security bullets. Codifly lists them by name.
- **low** · add to context/ if true: If you worked in Scrum or Kanban (sprints, reviews, Jira) at Nexits, Talan or K-Rose, add it to one bullet.
- **low** · resume edit: Trim the skills that don't serve this offer (Astro.js, Vue.js, Electron, Terraform, Keycloak, SQLite) and keep the React/Node/GraphQL/testing/security lines tight.
- **low** · gap to close: Build a small React Native app or a GraphQL + Apollo Server project to cover the bonus and Apollo gaps.

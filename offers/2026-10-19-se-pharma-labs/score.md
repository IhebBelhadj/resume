# Resume score: 6.5/10

_2026-10-19-se-pharma-labs, scored by claude-opus-5-5_

Maybe, leaning toward a shortlist. The listed must-haves are all soft skills, and your resume backs most of them: you show ownership ("Built a Python tool on my own", "lead of a 3-developer team"), English at C1, and customer contact ("Joined calls with the client's validation and data teams (GRDF)"). Your best match is the data-mapping work. Converting XML from SOAP-based CRM/ERP systems into 100+ Snowflake models is close to "convert and map structured and semi-structured customer data", and you also have React/TypeScript and testing evidence. The problem is the first task in the offer: production backend code in Rust. Your resume has no Rust at all. Kubernetes and Ansible appear only in a personal lab, and there is nothing on MLOps or manufacturing. With 100+ applicants, a Rust shop will put people who have written Rust ahead of you. The summary doesn't help either: it is generic and doesn't point to the ERP data-integration angle, which is the one thing that sets you apart.

## Weaknesses

- There is no Rust anywhere on your resume. Rust isn't in your Languages line, your projects or your stacks, yet the first task in the offer is "Develop production-ready backend code in Rust". It is only a nice-to-have, but it is the language you would write every day.
- All of your Kubernetes and Ansible experience comes from OpsForge, a personal lab. Your professional deployment work is Docker on EC2 with Terraform at Nexits, and you describe it as "Worked with the team on" and "Contributed to". Nothing shows you deploying or operating services on Kubernetes in production.
- Your Talan intern bullet ends with "In effect, this rebuilt by hand what Kubernetes provides out of the box". That reads as a remark against your own work and spends the line on commentary instead of results.
- The summary is generic ("working across full-stack products and data platforms"). It doesn't name your strongest matches for this role: mapping ERP/CRM XML data into internal models, customer-facing calls, and production debugging. As a result, the top third of the page doesn't make the case for this job.
- Nothing shows MLOps or work alongside an ML team. LangGraph appears only in skills and stacks, with no bullet behind it.
- Nothing shows manufacturing, industrial software or ERP/MES integration beyond the CRM/ERP XML conversion.
- Two entries are empty: Nexits "Freelance Job" and the Nexits internship. They take up space, and "Freelance Job" is a weak title.
- The Networking skills line (mDNS / DNS-SD, tc/netem, UDP, OAuth Device Flow) and parts of the long DevOps line add clutter for a backend/integration role.
- "Saving weeks of manual work" is a vague result next to otherwise concrete numbers.
- Your phone number is +216 and all your locations are in Tunisia or France, while the role is remote in Germany. Nothing says whether you can work from there (EU residence, work authorization, time zone).

## Strengths

- Strong data-mapping evidence: you converted "XML data from SOAP-based CRM and ERP systems into 100+ Snowflake models across 20+ migrated workflows" with a tool you built, which has an enforced schema, validation and lineage. This lines up directly with "Convert and map structured and semi-structured customer data".
- Customer interaction is backed by a concrete example: calls with GRDF's validation and data teams to investigate production anomalies.
- Ownership and architecture are evidenced: you "Led the architecture of multi-environment Airflow orchestration for 850+ DAGs", and you wrote the architecture plan for K-Rose and built and deployed it end to end as lead of 3 developers.
- Real React/TypeScript frontend work: the K-Rose Next.js app, plus the Playpex React admin dashboard built on generated API types.
- API design evidence: "versioned REST API specified in OpenAPI 3.1, a contract test against the spec and uniform error codes".
- Testing and production operations: Vitest unit tests, an integration test using TDD, Sentry/Axiom monitoring, separate staging/prod AWS accounts, and promotion by digest behind an approval gate.
- Your OpsForge bullets are concrete and hands-on: K3s, Ansible roles, Flux GitOps, and fault-injection scenarios with pass/fail checks.
- Your bullets are mostly concrete about what you built, with which tools and at what scale.

## Requirements

| | Requirement | Evidence in the resume |
|---|---|---|
| ✅ | Strong willingness to learn and take ownership (must) | Built a Python tool on my own...; Led the architecture of multi-environment (dev, test, prod) Airflow orchestration for 850+ DAGs |
| ⚠️ | Flexibility to grow with the role as responsibilities evolve (must) | Breadth across data platform (Talan), full-stack (K-Rose, Nexits) and infra (OpsForge); not stated explicitly |
| ⚠️ | Collaborative spirit, comfort in a flat hierarchy (must) | built and deployed it end to end as lead of a 3-developer team; Worked with the team on deploying the SaaS to AWS |
| ✅ | Good English communication, written and spoken (must) | English (C1); Joined calls with the client's validation and data teams (GRDF)... and explain the analysis |
| ⚠️ | Manage time, tasks and priorities independently (must) | Lead Full-stack Engineer (Freelance, part-time) alongside full-time Talan role; solo-built tool and projects |
| ❌ | 1+ year of Rust experience (nice) | — |
| ✅ | Experience building frontends, ideally React (nice) | one Next.js/TypeScript app with a public site, a client portal and a Payload CMS back office; Built the React admin dashboard (Vite, Tailwind CSS, shadcn/ui, TanStack Query) |
| ⚠️ | DevOps experience, e.g. Kubernetes, Ansible (nice) | OpsForge (personal): idempotent Ansible roles... K3s Kubernetes cluster... Flux GitOps; professional: Terraform/AWS, GitHub Actions CI/CD at Nexits |
| ✅ | Experience joining calls and interacting with customers (nice) | Joined calls with the client's validation and data teams (GRDF) to investigate production anomalies |
| ❌ | Experience in manufacturing or industrial software (nice) | — |
| ⚠️ | Task: interface with customer ERP/MES systems and map customer data into internal formats | convert XML data from SOAP-based CRM and ERP systems into 100+ Snowflake models across 20+ migrated workflows |
| ✅ | Task: unit and integration tests | Wrote Vitest unit tests for the auth flows and an integration test for the contact API using TDD; contract test against the spec |
| ⚠️ | Task: debug and resolve issues in staging and production | investigate production anomalies in legacy pipelines; Tracked production errors with Sentry |
| ✅ | Task: contribute to API design and system architecture | versioned REST API specified in OpenAPI 3.1; Wrote the architecture plan for kairouanrose.com |
| ❌ | Task: support MLOps workflows with the ML team | — |

## To raise the score

- **high** · gap to close: Close the Rust gap before applying. Build a small Rust backend service (for example Axum or Actix with Postgres, plus unit and integration tests), ideally one that ingests and maps an ERP-style CSV or XML export. Put it on GitHub and add it as a project.
- **high** · add to context/ if true: If you have written any Rust at all (coursework, side projects, contributions), add it to Languages and give it a project line.
- **medium** · resume edit: Rewrite the summary around this role. Lead with mapping customer ERP/CRM data (SOAP/XML) into internal models, customer-facing requirement and anomaly calls, and taking features from requirements to production. Then add React/TypeScript and the Kubernetes/Ansible lab.
- **medium** · resume edit: Cut the sentence "In effect, this rebuilt by hand what Kubernetes provides out of the box" from the Talan intern bullet. Spend the space on what the platform enabled.
- **medium** · add to context/ if true: If you have deployed or operated anything on Kubernetes outside OpsForge, or worked with ML models or pipelines in production (training, serving, data prep for an ML team), add it.
- **medium** · add to context/ if true: If you have touched manufacturing, logistics, supply-chain or ERP/MES data (including in the GRDF or K-Rose order and delivery work), state it in those terms.
- **medium** · add to context/ if true: If you live in the EU, have German or EU work authorization, or can work on CET hours, say so in the header or summary.
- **low** · resume edit: Drop the empty Nexits "Freelance Job" and Nexits internship entries, or merge them into the Nexits Full-stack Developer line as dates only.
- **low** · resume edit: Trim the Networking skills line and shorten the DevOps list to what this role uses (Kubernetes, Ansible, Terraform, Docker, GitHub Actions, AWS). Move Rust-adjacent backend skills higher.
- **low** · resume edit: Change "Built a Python tool on my own" to a stronger opener such as "Designed and built, solo, a Python tool...". Swap "saving weeks of manual work" for a concrete figure if one exists in your records.

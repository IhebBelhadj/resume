# Resume score: 7.4/10

_2026-10-17-kpmg-data-eng, scored by claude-opus-5-5_

I would shortlist you. Your technical core fits this junior data-engineering consulting role better than most junior applicants. You already work as a Data Engineering Consultant at Talan, a consulting firm, on dbt, Snowflake, Airflow and Informatica, you hold an engineering degree, and you have real full-stack experience with React/Next.js, PostgreSQL, AWS and Docker. That covers the offer's "Back-End, Front-End, ETL" profile. The score stays below 8 because the consultant side of the role has almost no evidence. The offer starts with requirements gathering from business teams and writing specifications, then testing (recette) and documentation, and your resume barely shows any of these. A screener will also see that several skills the offer names (Spark, Databricks, C#, MySQL, MongoDB) appear only in your skills list, with no experience behind them. Azure, GCP, Git and D3.js do not appear anywhere.

## Weaknesses

- The consultant side of the job has almost no evidence. The offer's first two missions are "recueil des besoins de différents métiers" (gathering requirements from business teams) and "conception de cahier des charges et/ou spécifications fonctionnelles" (writing specifications). Your only related line is "Rédaction du document d'architecture" at K-Rose, which is a technical document, not a functional one. No bullet shows you working with business users, clients or a functional specification.
- Several skills the offer names appear only in your skills list. "Big Data (Spark, Databricks, Kafka)", C#, MySQL and MongoDB are listed under skills, but no experience mentions them. A recruiter will treat these as keywords and question you on them in interview.
- Some of the offer's tools are missing entirely. Azure and GCP are not on the resume (only AWS), and neither are Azure DevOps or D3.js. Git is never named: the only hint is "revue et merge des pull requests".
- Your bullets describe tasks but give no results. "Pilotage de la migration d'un projet d'intégration de données CRM vers dbt et Snowflake" gives no volume, number of models, timeline or outcome. "Correction des anomalies" for GRDF gives no scale or impact. The only figures on the page are "plus de 100 colonnes par modèle" and "rollback en ~10 s".
- Testing (recette) and documentation are not shown. You list Pytest, Vitest, Playwright and SonarQube in skills, but no bullet says you tested or documented anything, and the offer names "recette, documentation et maintenance" as a mission.
- Machine Learning is thin. The only mention is "des prévisions par Machine Learning" inside a pipeline bullet, with no model, method or result.
- The "Software Engineering Intern – Nexits" entry has no bullets and no stack. It takes a line of a one-page resume and says nothing.
- You have no languages section. A consulting role with France–Maghreb mobility and international projects will expect your French and English levels.
- The skills section repeats itself: "Cloud (AWS, Vercel)" is followed by "AWS EC2, S3, AWS RDS, AWS CloudFront". Date formatting is also inconsistent: Nexits dates use a hyphen ("nov. 2024 - févr. 2025") while the others use an en dash.

## Strengths

- Your current job matches the target closely: "Data Engineering Consultant, Talan" since Oct. 2025, a data role at a consulting firm. That is the same profile as "Consultant Débutant Data Engineer".
- You have concrete ETL/ELT and orchestration work: a migration to dbt and Snowflake, Airflow orchestration across environments with DAGs triggered by data assets, and a Python tool that generates SQL from Informatica mappings ("plus de 100 colonnes par modèle, lineage").
- You show the full chain the offer describes ("solutions Data Analytics… industrialisation… applications full stack"): an end-to-end pipeline with MinIO, Airflow, Airbyte and dbt plus ML forecasting, real-time CDC (change data capture) feeding live charts, and a full-stack B2B platform you designed, built and deployed.
- Your cloud and Docker experience is real: AWS with Terraform (S3 + CloudFront, EC2 with Docker Compose, RDS PostgreSQL) and CI with GitHub Actions at Nexits.
- Your React/Next.js front-end experience comes from two separate jobs (K-Rose, Nexits), which covers "Connaissance des frameworks Front-End (React…)".
- Production maintenance for a named client ("Maintenance en production avec GRDF") answers the offer's "maintenance des applications".
- Your AI work (LangGraph multi-agent SQL and chart generation, conversion of Informatica mappings to dbt with agentic AI) fits the team's "Data & Analytics et d'intelligence artificielle" focus.
- The first third of the page makes your case: a French summary that names the consulting role, the engineering degree and the offer's stack, then your strongest experience at the top.

## Requirements

| | Requirement | Evidence in the resume |
|---|---|---|
| ✅ | Diplômé(e) d'une école d'ingénieur (engineering-school graduate) | Diplôme d'ingénieur en génie logiciel, ESPRIT, sept. 2022 – sept. 2025 |
| ✅ | Première expérience en développement applicatif et Data (Back-End, Front-End, ETL, Machine Learning) | Data Engineering Consultant, Talan (dbt, Snowflake, Airflow); Lead Full-stack Engineer, K-Rose (Next.js, PostgreSQL); "des prévisions par Machine Learning" (ML evidence is thin) |
| ✅ | Maîtrise d'un ou plusieurs langages (Python, Spark, C#, Java…) | Python and SQL in the Talan stacks; Java and C# listed under Langages; Spark listed under skills only |
| ✅ | Bases de données (MySQL, PostgreSQL, MongoDB…) | PostgreSQL in the K-Rose, Nexits and Talan intern stacks; "RDS PostgreSQL"; MySQL and MongoDB listed under skills only |
| ⚠️ | Environnements Cloud (Azure, AWS, GCP, Databricks) | AWS with Terraform: S3 + CloudFront, EC2, RDS (Nexits); Snowflake; no Azure or GCP; Databricks listed under skills only |
| ✅ | Connaissance des frameworks Front-End (React, D3.js…) | React and Next.js in the K-Rose and Nexits stacks; no D3.js |
| ⚠️ | Outils de versioning (Git, Azure DevOps…) | "revue et merge des pull requests"; CI/CD (GitHub Actions); Git itself is never named |
| ✅ | Idéalement Docker (nice-to-have) | "CMS sur EC2 avec Docker Compose"; Docker, Docker Compose under Cloud & DevOps |
| ❌ | Recueil des besoins métiers (Finance, RH, Risk…) chez les clients (gathering requirements from business teams) | — |
| ⚠️ | Conception de cahier des charges / spécifications fonctionnelles (writing specifications) | "Rédaction du document d'architecture" (K-Rose); technical, not functional |
| ✅ | Développement de solutions Data Analytics / Big Data et industrialisation en applications full stack, souvent en cloud | "pipeline de données de bout en bout (MinIO, Airflow, Airbyte, dbt)", "pipeline CDC temps réel", a full-stack B2B platform deployed end to end |
| ⚠️ | Recette, documentation et maintenance des applications (testing, documentation, maintenance) | "Maintenance en production avec GRDF"; Pytest, Playwright and SonarQube listed under skills; no testing or documentation bullet |
| ✅ | Contexte conseil / missions clients (consulting context) | Data Engineering Consultant at Talan; client maintenance for GRDF |

## To raise the score

- **high** · add to context/ if true: If you have met business or client teams at Talan or GRDF to gather requirements, or written functional specifications or mapping specs, add a bullet that says so: who you worked with, what you produced, and for which project.
- **medium** · add to context/ if true: If you know the scale or outcome of the CRM migration to dbt and Snowflake (number of models or tables, data volumes, number of environments, timeline, conversion time saved by the AI tool), add it to the relevant Talan bullets.
- **medium** · add to context/ if true: If you wrote tests (dbt tests, Pytest, data-quality checks), ran testing phases (recette) or wrote technical or user documentation on any of these projects, add a bullet. The offer names "recette, documentation" as a mission.
- **medium** · add to context/ if true: If you have used Git (your pull-request reviews suggest so), name it explicitly in Cloud & DevOps. It is a named requirement and currently appears nowhere.
- **medium** · add to context/ if true: Add a languages section with your French and English levels. A consulting role with France–Maghreb mobility will screen for these.
- **medium** · gap to close: Get hands-on experience with Azure (Data Factory or Synapse) or Databricks/PySpark, for example through a certification such as DP-203 or Databricks Data Engineer Associate, or a small project. Both are named in the offer and common at KPMG's clients.
- **low** · resume edit: Either back Spark, Databricks, Kafka, C#, MySQL and MongoDB with an experience or project line that shows them, or drop the ones you can't defend in interview, so your skills list matches your experience.
- **low** · resume edit: Remove the empty "Software Engineering Intern – Nexits" entry, or merge it into the Nexits line. It uses space and says nothing.
- **low** · resume edit: Remove the duplicates under Cloud & DevOps ("Cloud (AWS, Vercel)" followed by "AWS EC2, S3, AWS RDS, AWS CloudFront"), for example by writing "AWS (EC2, S3, RDS, CloudFront)". Also use en dashes in all date ranges.
- **low** · add to context/ if true: If the live CDC charts or the LangGraph chart generation used a data-visualisation library (D3.js, Recharts, ECharts…), name it. The offer cites D3.js.
- **low** · add to context/ if true: If you can say more about the ML forecasting step (model, features, evaluation), add it, since ML is part of the offer's profile.

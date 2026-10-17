---
id: nexits-fullstack
company: Nexits
titles: [Full-stack Developer, Software Engineer]
location: Paris, FR (Remote)
start: 2023-08
dates: Aug 2023 - Sep 2024
tags: [fullstack, nextjs, trpc, aws, monorepo, devops, terraform]
stack:
  - Next.js
  - React
  - Vue.js
  - TypeScript
  - Node.js
  - tRPC
  - PostgreSQL
  - AWS
  - AWS EC2
  - AWS ECR
  - S3
  - AWS RDS
  - AWS CloudFront
  - AWS SSM
  - AWS IAM
  - AWS EventBridge
  - AWS CloudWatch
  - AWS CloudTrail
  - AWS GuardDuty
  - Terraform
  - Docker
  - Docker Compose
  - Caddy
  - pg-boss
  - GitHub Actions
  - Turborepo
  - Zustand
  - Sentry
---

<!-- Raw facts: never rendered. Resume bullets are generated from this text per offer and
     must quote it as their source, so write everything down (scope, team, tools, numbers,
     what you only touched). Keep it true; vague is fine, inflated is not. -->

## Context

- Nexits is a small startup: everyone does cloud, DevOps and software engineering, so the team
  did pretty much all of it together.
- When I joined, Nexits had a WordPress website and a product written in Vue.js. We first worked
  on the Vue.js app; in parallel we created a Turborepo monorepo meant to hold everything,
  starting with the SaaS product (the migration to Next.js, tRPC and Turborepo).
- I left in Sep 2024 with the monorepo and the SaaS in their initial setup. Nexits later called
  me back as a freelancer for the landing website in the same monorepo (see nexits-freelance).
- TODO: what the SaaS product does; team size.

## Deployment of the SaaS on AWS

- The team hosted the SaaS following a deployment plan ("AWS Deployment Plan: SaaS (frontend +
  backend) in the Nexits Monorepo"). It had a cost-first **launch profile** and a later "growth"
  architecture (ECS Fargate, ALB, Aurora, SQS, Valkey, WAF, a shared account); **only the launch
  profile was built**, so never claim ECS, Fargate, ALB, Aurora, SQS, Valkey or WAF here.
- My part: I worked on a bit of everything (plan, Terraform, CI/CD, host and Docker setup)
  alongside the team. Say "with the team" / "worked on", not "alone" or "led".
- The saved copy of the plan is a later version that also co-hosts the landing CMS on the same
  instance (that part belongs to nexits-freelance); bullets here stay on the SaaS.
- Separate AWS accounts per environment (management, staging, prod) under AWS Organizations;
  ECR in prod, staging pulls cross-account, so prod never depends on staging.
- Terraform: one state per stack per account (network with public subnets for the host and
  private subnets for the database and no NAT gateway, host, data, web), stacks sharing outputs
  through SSM Parameter Store instead of remote state.
- API and background worker as containers on an **EC2 Graviton instance** with **Docker
  Compose** (same image, different command); migrations run as a one-off container with a
  separate database owner role before the API rolls.
- **Zero-downtime API deploys** with docker rollout: scale the API to 2, wait for the new
  container's health check, stop the old one; Caddy retries during the swap; graceful SIGTERM
  draining.
- API reachable only through CloudFront: `app.<domain>/api/*` → origin hostname → Caddy, which
  rejects any request without a secret origin header; same-origin API, so no CORS and host-only
  session cookies.
- Database: **RDS PostgreSQL** (single-AZ, private subnets, 7-day point-in-time recovery,
  deletion protection, master password managed by AWS), an app role without BYPASSRLS for the
  API and worker and an owner role for migrations only. Quarterly restore drill planned.
- Jobs, retries, dead-letter queues and cron schedules with **pg-boss** on the same Postgres
  instead of a separate queue service; versioned job payloads.
- User uploads on S3 with presigned PUT/GET, versioning, noncurrent versions expire after 30 days.
- Frontend served from S3 + CloudFront with immutable releases and a KeyValueStore release
  pointer (instant switch and ~10 s rollback), runtime `config.json` per environment so the same
  build goes to staging and prod.
- Staging on a smaller EC2 instance with a Postgres container, stopped at night and on weekends
  by **EventBridge Scheduler**; CI starts it on demand before deploying.
- CI/CD with **GitHub Actions** and GitHub OIDC → AWS STS role assumption (no long-lived keys),
  least-privilege deploy roles per account. Build once, promote the artifact: the image is
  built once (arm64), deployed **by digest** to staging then prod; fixed deploy order
  migrate → api → worker → web; expand-only (backward-compatible) migrations, drops in a later
  release; staging → tests → manual approval gate → prod.
- Affected-app detection from the Turborepo graph (`turbo ls --filter="...[base]"`) instead of
  hand-written path filters, so only changed apps and their dependents are rebuilt.
- Secrets in SSM Parameter Store, one env file per service. Monitoring: CloudTrail, GuardDuty
  in prod, Sentry, an external uptime check.
- TODO: confirm which of these parts of the plan were actually in place when you left (Sep
  2024): Postgres Row-Level Security per tenant and its isolation tests, Playwright e2e on
  staging, PR previews, the web app as a Vite SPA vs Next.js.

## Numbers

- Planned launch cost about $70–75/month vs about $600/month for the growth architecture
  (plan estimates, not a measured bill; the $70–75 includes the landing site and CMS).

## From past resumes

- Implemented product state historization with audit trail, enabling edits, rollbacks, and time-travel of product data.
- Contributed to migration from legacy stack to Next.js, tRPC, and Turborepo monorepo with AWS deployment.
- Contributed to GitHub Actions CI/CD pipelines for the Turborepo monorepo, orchestrating builds, tests, and deployments across multiple services, enabling faster consistent environment delivery for the entire team.
- Contributed to a frontend platform by building reusable components and a hybrid state management system with route-based state and Zustand, optimizing load times and UX.

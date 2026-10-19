---
id: nexits-freelance
company: Nexits
titles: [Freelance Full-stack Developer, Freelance Software Engineer]
location: Paris, FR (Remote)
start: 2024-11
dates: Nov 2024 – Feb 2025
tags: [frontend, cms, astro, performance, aws, devops, terraform]
stack:
  - Astro.js
  - Payload CMS
  - Next.js
  - React
  - TypeScript
  - SQLite
  - Turborepo
  - AWS
  - AWS EC2
  - AWS CloudFront
  - S3
  - AWS ECR
  - AWS SSM
  - AWS IAM
  - AWS Route 53
  - AWS CloudWatch
  - Terraform
  - Docker
  - Docker Compose
  - Caddy
  - Litestream
  - GitHub Actions
  - Vercel
---

<!-- Raw facts: never rendered. Resume bullets are generated from this text per offer and
     must quote it as their source, so write everything down (scope, team, tools, numbers,
     what you only touched). Keep it true; vague is fine, inflated is not. -->

## Context

- Freelance mission for Nexits (same company as nexits-fullstack): after I left in Sep 2024,
  Nexits called me back to build the Nexits marketing / landing website (replacing their old
  WordPress site) inside the same Turborepo monorepo as the SaaS, with pages that non-developers
  can build and edit from a CMS, with live preview, and to host it on AWS.
- The client (Nexits) gave a brief and a starter monorepo template; code was reviewed before approval.
  Brief: Astro.js, mostly statically generated for performance and SEO; Astro components for static
  content + React for interactive parts; minimal dependencies (Tailwind CSS, Framer Motion, shadcn);
  sitemap + SEO integrations; Payload CMS v3 for live content editing; linting and type-checking that
  work across the monorepo.
  monorepo with the rest of the Nexits apps and was hosted on AWS (see Deployment below).
- Iheb worked alone on the website and CMS code, with code reviews and feedback from the Nexits
  team. The project was delivered in about 4 months (Nov 2024 – Feb 2025).

## What I did

### CMS and block-based page builder (Payload CMS v3)

- Set up Payload CMS v3 running inside Next.js 15 (App Router) as the admin app, with SQLite
  (`@payloadcms/db-sqlite`) as the content database in this version.
- Designed the collections: Users, Media, Pages, Plans, FAQs, EnterpriseContacts; globals Header
  (navigation items) and Infos (site name, logos).
- Designed a nested, block-based page model so editors compose whole pages without code:
  a page = one hero block + an array of section blocks → content blocks with a layout type
  (single / two / three / four columns, display grid) → column blocks (media, rich text, card,
  hoverable card, features, pricing, FAQs, CTA).
- Reusable CMS fields: link (internal page reference or external URL), slug (custom admin component), icon.
- Pages collection: drafts with 100 ms autosave (for live preview), SEO tab fields, slug, access
  rules (pages readable only when published in production), redirects and SEO plugins.
- Lexical rich-text editor; Payload REST API consumed by the site.

### Live preview ("on the fly" page building)

- Live preview: Payload's live preview iframes an SSR'd `/preview/[slug]` route of the Astro site that
  fetches draft content and reloads on Payload document events, so editors see the page update as
  they build it. Preview images are served live from the CMS.
- Dual rendering strategy: SSR for the preview route, SSG (static prerendering) for production pages.

### Astro site and rendering pipeline

- Astro 5 site: at build time it fetches published pages and globals from the Payload REST API,
  downloads all media into the static build, and prerenders one page per CMS slug.
- Wrote the renderer chain that maps CMS blocks to components: layout → header / hero → sections →
  layout grids → column blocks, through a block-type → component mapping (adding a CMS block =
  adding a mapping entry). Rich-text and media parsers, pricing block renderer, link resolver.
- React islands hydrated only when visible (`client:visible`) for minimal client JS; nanostores for
  site-wide state (site infos, logos, preview flag).
- Site optimisation: asset prefetching, caching policy, changed JS loading policy, resource
  compression (astro-compress), favicon fixes; sitemap, MDX blog (separate from the CMS), RSS, astro-icon.

### Shared UI library and monorepo

- Built the shared React component package: shadcn/ui primitives, Magic UI animated components,
  page blocks (header, footer, CTA, pricing, features, carousels), hero components, layout grids
  matching the CMS layout types, chart components. Tailwind CSS.
- pnpm + Turborepo monorepo: apps (admin, landing) + packages (ui, shared types, zod validators) +
  shared tooling configs (ESLint presets incl. Astro, Prettier, Tailwind, TypeScript strictest).
- Shared generated Payload types package so the Astro site types CMS responses without depending on
  the admin app (a type-generation script regenerates and copies them).
- Fixed linting/formatting across the repo; GitHub Actions CI runs lint, workspace dependency lint
  (sherif), format check and typecheck. No test suite.

### Deployment on AWS (landing site + Payload CMS + preview)

- I wrote the deployment plan for the landing site and the CMS ("AWS Deployment Plan: Nexits
  Landing + Payload CMS"). It had a cost-first **launch profile** and a later "growth"
  architecture (ECS Fargate, ALB, RDS, WAF); **only the launch profile was built**, so never
  claim ECS, Fargate, ALB, WAF or RDS for this mission.
- Nexits is a small startup where everyone does cloud, DevOps and software work: the team built
  the hosting together following the plan, and I worked on every part of it (plan, Terraform,
  CI/CD, host and Docker setup). Say "built with the team" / "worked on", not "alone".
- Infrastructure as code with **Terraform**: a bootstrap stack applied once by hand (S3 state
  bucket with versioning and S3-native locking `use_lockfile`, so no DynamoDB table; the GitHub
  OIDC provider; the CI IAM roles), then stacks for network (VPC, public subnets only, no NAT
  gateway), static site, host, ECR, DNS (Route 53) and budget. Default tags Project / Env.
- **No long-lived AWS keys anywhere**: GitHub Actions authenticates with GitHub OIDC → AWS STS
  `AssumeRoleWithWebIdentity`, with least-privilege IAM roles per workflow (tf-plan read-only,
  tf-apply behind a GitHub environment with a required reviewer and a permissions boundary that
  stops CI from editing its own roles, deploy-site, deploy-host), trust policies matching the
  exact `sub` claim (repo + GitHub environment).
- **Static site on S3 + CloudFront** with atomic, immutable releases: each build is uploaded to
  `releases/<id>/`, a CloudFront Function reads the current release id from a CloudFront
  KeyValueStore and rewrites the request at viewer-request, so switching the pointer releases
  instantly with no CloudFront invalidations, and a rollback (workflow_dispatch) is one
  KeyValueStore write (~10 seconds). Upload → smoke test → pointer flip, last 10 releases kept.
- Per-object Cache-Control: hashed assets immutable for a year, HTML revalidated by browsers
  but cached per release at the edge; security headers (HSTS, CSP…) and a custom 404.
- CMS publish → rebuild: a Payload hook calls GitHub `repository_dispatch`, which rebuilds and
  releases the static site (about 2–4 min from publish to live); a GitHub Actions concurrency
  group coalesces bursts of publishes into at most two builds.
- CMS and preview on **one EC2 Graviton instance (t4g.small)** running **Docker Compose**: Caddy
  (automatic Let's Encrypt TLS, routing for the cms. and preview. hosts), Payload CMS (Next.js
  standalone image), the Astro SSR preview, and **Litestream** replicating the SQLite database to
  S3 (60 s sync, 7 days retention). Media on S3 served through the site's CloudFront distribution.
- Deploys through **AWS SSM Run Command**: CI builds arm64 images (turbo prune multi-stage
  Dockerfiles, non-root), pushes them to ECR, then runs a restricted SSM document that only
  accepts a service name and an image pinned by digest; the deploy script waits for the health
  check and rolls back to the previous image if it fails. No SSH: port 22 closed, shell access
  through SSM Session Manager; secrets in SSM Parameter Store, rendered into one env file per service.
- Reliability on a budget: CloudWatch alarm with EC2 auto-recover, daily EBS snapshots (DLM, 7
  kept), logs to CloudWatch (14 days), the static site stays up from CloudFront if the host is
  down; the host is disposable and rebuilt from Terraform + Litestream restore in about 10 min
  (disaster drill: terminate the host, apply, check the content is restored).
- Security fixes found while preparing the deploy: removed a leftover Payload route that
  exposed every user record through the Local API, login brute-force protection
  (`maxLoginAttempts` 5, 10 min lock) instead of paying for a WAF, IMDSv2 required.
- Cost hygiene: AWS Budgets alerts, Cost Anomaly Detection, retention limits on logs, images,
  releases and snapshots.

## Numbers

- Lighthouse: 100 performance, 95 accessibility, 100 SEO (from past resumes; TODO: confirm on which page/build).
- Hosting cost: about $25/month for the launch profile
- Rollback ~10 s; publish to live ~2–4 min; host rebuild ~10 min.

## From past resumes

- Architected a CMS solution with Payload CMS and a custom block-based page builder, enabling no-code content updates for the landing site.
  - Architected a CMS solution with Payload CMS and a custom block-based page builder, integrating it into the existing Nexits Turborepo monorepo and GitHub CI/CD pipeline, enabling no-code content updates for the landing site.
- Built an instantaneous preview system using Astro.js for dynamic component rendering with minimal JS.
- Designed a dual rendering strategy (SSR for preview, SSG for production), achieving 100 performance, 95 accessibility, and 100 SEO score on Lighthouse.

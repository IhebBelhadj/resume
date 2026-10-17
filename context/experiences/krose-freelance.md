---
id: krose-freelance
company: K-Rose
website created: https://www.kairouanrose.com/
titles:
  [
    Freelance Job,
    Freelance Software Engineer,
    Lead Full-stack Engineer (Freelance),
  ]
location: Tunis, TN
start: 2026-02
dates: Feb 2026 – May 2026
tags: [fullstack, frontend, backend, nextjs, cms, ecommerce, b2b, i18n]
stack:
  [
    Next.js,
    React,
    TypeScript,
    Payload CMS,
    PostgreSQL,
    Drizzle ORM,
    Neon Postgres,
    Clerk,
    Tailwind CSS,
    shadcn/ui,
    GSAP,
    Framer Motion,
    Resend,
    React Email,
    Upstash Redis,
    Axiom,
    Vercel,
    Vercel Blob,
    Vitest,
    Playwright,
    Zod,
    SWR,
    TanStack Table,
    Docker,
    Sentry,
  ]
repo: /home/iheb/projects/kairouan-rose
---

<!-- Raw facts: never rendered. Resume bullets are generated from this text per offer and
     must quote it as their source, so write everything down (scope, team, tools, numbers,
     what you only touched). Keep it true; vague is fine, inflated is not. -->

## Context

- Client: Kairouan Rose (K-Rose, legal name STE KAIROUAN ROSE), a Tunisian producer of Damascus rose products (rose hydrolat, petals, dried rose, rose essential oil) that sells directly to businesses. Live at [kairouanrose.com](https://www.kairouanrose.com/).
- B2B: products are sold per kg at prices negotiated per client and per order, so there is no public price list; every order starts as a request, goes through negotiation (meeting + price agreement), then becomes a confirmed order with a delivery schedule.
- The platform replaces email, phone calls and spreadsheets with a public website, a client portal and a back office, all in one Next.js app.
- Team: me and two other developers. The repository is mine; I made about 140 of its 164 commits, wrote the platform plan / architecture document, reviewed and merged the pull requests, and built and deployed the platform end to end.
- What the other two developers did (not me): one built the contact form email logic, React Email templates, the FAQ component, GSAP scroll animations on the sections, the blog section and a footer / language selector redesign; the other set up the sign-up workflow for client users with Payload client registration, the initial Payload collections and the landing page globals.
- Repo history runs from Dec 2025 to Aug 2026 (marketing site Jan–Mar 2026, client portal Mar 2026, CMS-managed SEO May 2026, orders / deliveries / meetings back office Aug 2026). TODO: confirm the contract dates (the resume says Feb 2026 – May 2026).

## Architecture

- One Next.js 15 (App Router) app with React 19 and TypeScript (strict) and three parts: a public marketing site, a Clerk-authenticated client portal, and the Payload CMS 3 admin panel as back office.
- Payload CMS is the business database and the content backend: PostgreSQL through Payload's Postgres adapter (Drizzle), versioned database migrations, generated TypeScript types.
- Clerk handles client identity only; Payload holds the business data. The two are bridged by storing the Clerk user id on a Payload `clients` record, created at sign-up; if that write fails, the Clerk user is deleted so no partial account is left. Payload's own users are the admins.
- Next.js middleware: Clerk auth, redirects for signed-in / signed-out users on the portal, then locale routing with next-i18n-router.
- Server Actions and API route handlers call the Payload local API and resolve the Clerk user to its client record on every request.
- Media storage on Vercel Blob; deployed on Vercel. Local Postgres via Docker Compose.

## Public website

- Trilingual: French (default), English and Arabic, with Payload field localization plus route-level dictionaries typed so a key missing in one language is a TypeScript error. Arabic is right-to-left on the product pages and the invoice.
- Per-page SEO metadata (titles, descriptions, Open Graph) editable from the CMS in all three languages, cached with Next.js `unstable_cache` and invalidated by tag (`revalidateTag`) when the page is saved in the CMS.
- Tag- and path-based cache revalidation from Payload hooks for posts, products, redirects and the company contact global, with a `disableRevalidate` context flag to skip revalidation (e.g. during bulk imports).
- Automatic sitemaps (next-sitemap, posts and products sitemaps), structured company data (JSON-LD) generated from a CMS global, CMS-managed redirects.
- Blog (Payload Lexical rich text, posts, categories), product pages, about carousel, footer, contact details all editable from the CMS.
- Animated UI: GSAP timelines (page loader, hero, parallax leaves), Framer Motion, custom cursor, glass-morphism cards, expandable service cards, interactive map with double-tap on mobile, Calendly meeting booking popup.
- Performance work for mobile and low-end devices: removed expensive elements on mobile, changed component mounting logic, disabled 3D rotation on mobile, lazy-loaded images, and a hook that detects low-end devices to serve a lighter Tailwind variant.
- Contact form with email through Resend and React Email templates, protected by Upstash Redis rate limiting and bot protection.
- Vercel Analytics behind a cookie consent banner.

## Client portal

- Clerk sign-in / sign-up with email verification, multi-step sign-up whose intermediate state persists, translated auth pages.
- Three-step order wizard (choose, configure, review) for three order types: express order, seasonal contract (delivery batches) and pre-order; forms built with react-hook-form and Zod.
- Ready-date picker on a calendar that colours each day by production load (low / medium / high), computed from the kg already committed in live orders against a daily capacity set in the CMS.
- Pickup or delivery per order, delivery fees per shipment.
- Orders list (TanStack Table with filters), order detail page with its deliveries, client-side cancellation allowed only in the statuses where it is still safe.
- Notifications panel (SWR, optimistic read / unread) and a banner on order updates; meetings shown on a calendar (react-big-calendar).
- Clients see only their own orders, deliveries, addresses and notifications: Payload access functions resolve the Clerk user to its client record and filter on the server.

## Back office (Payload admin)

- Admin dashboard replaced by a custom month / week / day operations calendar of deliveries and meetings.
- Collections for clients, orders, deliveries, addresses, meetings, notifications, audit logs, products, posts, pages, media; grouped as CRM, catalogue, operations and settings.
- Orders: auto-numbered by type (EX- / SC- / PO-), status state machine (pending review, confirmed, completed, rejected, cancelled) with separate transition matrices for admins and clients, enforced in Payload `beforeChange` hooks and kept in pure modules; clients can only change the status, every other field they submit is dropped (field whitelist).
- Duplicate order protection: unique idempotency key on orders, checked in the hook with the database unique constraint as backstop (the portal does not send the key yet).
- Deliveries: one record per shipment or pickup (one per seasonal batch), statuses scheduled / preparing / in transit / delivered, status history, carrier, tracking number, vehicle and driver, proof of delivery upload, delivery fee; quantity allocation and date guards against the parent order (an admin hint shows the kg left to allocate); deliveries sync back to their order.
- Meetings collection (negotiation meetings) linked to orders, created by admins.
- Printable HTML invoice per delivery (A4, localized, right-to-left aware).
- Audit log for orders and deliveries: field-level diff (from / to) of every change, actor (admin / client / system), IP and user agent, written in the same database transaction as the change; entries cannot be edited or deleted.
- Client notifications generated from the same diff when an admin updates an order or a delivery ("Status changed to ...").
- Live preview and drafts / versioning for content.
- PDF invoices (the invoice is HTML which the client prints to PDF)

## Observability, testing, tooling

- Structured logging to Axiom through next-axiom with contextual metadata in Server Actions and API routes, to inspect production errors.
- Vitest unit tests for the sign-up / sign-in flows and the client-creation action, an integration test for the contact API, Playwright set up for end-to-end tests.
- pnpm, ESLint, Prettier, Docker Compose for the local database.
- Wrote an internal issue tracker for the codebase (security, data integrity, routing, i18n, tests, tech debt) with priorities and fix directions.
- Used Sentry for error tracking for both client and server errors
- Used TDD development approach for development

## Not built (planned in the design document, do not claim)

- Online payments (Paymee), Calendly webhook, outbox / background jobs.

## Numbers

- Lighthouse on the production homepage, from my portfolio page: 92 performance, 97 accessibility, 96 best practices, 100 SEO.
- About 140 of the 164 commits in the repository are mine.

## From past resumes

- Lead the architecture and development of a B2B e-commerce platform for the floral industry **[kairouanrose.com](https://www.kairouanrose.com/)**, integrating a headless CMS as the backbone for both business operations (order, delivery, and product management) and content delivery (dynamic SEO rule sets, automated sitemap, and CMS-managed pages compiled as SSGs) — achieving Lighthouse scores of 98 SEO and 100 Accessibility.
- Implemented role-based access control with row-level ownership enforcement, mapping Clerk authentication to CMS domain entities across two independent layers
- Structured error logging via next-axiom with contextual metadata to inspect production errors
- Configured tag-scoped ISR cache invalidation tied to CMS publish events, with bulk-import-safe revalidation suppression
- Built a field-level audit logging system capturing structured diffs, actor metadata, and request context across all CMS collections
  - Note from the repo: the audit log covers orders and deliveries only, not all collections.

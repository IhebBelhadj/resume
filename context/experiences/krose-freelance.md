---
id: krose-freelance
company: K-Rose
website created: https://www.kairouanrose.com/
titles:
  [
    "Full-stack Engineer (Freelance, part-time)",
    Freelance Software Engineer,
    "Full-stack Engineer (Freelance)",
  ]
location: Tunis, TN
start: 2025-12
dates: Dec 2025 – Aug 2026
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
- What the other two developers did (not me): one built the contact form email logic, React Email templates, the FAQ component, GSAP scroll animations on the sections, the blog section and a footer / language selector redesign; the other set up the sign-up workflow for client users with Payload client registration, the initial Payload collections and the landing page globals.
- Contract: Dec 2025 – Aug 2026, matching the repo history (marketing site Jan–Mar 2026, client portal Mar 2026, CMS-managed SEO May 2026, orders / deliveries / meetings back office Aug 2026).
- Part-time freelance, done in evenings and on weekends alongside my full-time role at Talan.

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
- Reactive system that tracks the load of orders and deliveries, which prompt the client to choose a delivery day that limits the load on the production line
- Pickup or delivery per order, delivery fees per shipment.
- Orders list (TanStack Table with filters), order detail page with its deliveries, client-side cancellation allowed only in the statuses where it is still safe.
- Notifications panel (SWR, optimistic read / unread) and a banner on order updates; meetings shown on a calendar (react-big-calendar).
- Clients see only their own orders, deliveries, addresses and notifications: Payload access functions resolve the Clerk user to its client record and filter on the server.

## Back office (Payload admin)

- Admin dashboard replaced by a custom month / week / day operations calendar of deliveries and meetings.
- Collections for clients, orders, deliveries, addresses, meetings, notifications, audit logs, products, posts, pages, media; grouped as CRM, catalogue, operations and settings.
- Orders: auto-numbered by type, status state machine (pending review, confirmed, completed, rejected, cancelled) with separate transition matrices for admins and clients, enforced in Payload `beforeChange` hooks and kept in pure modules; clients can only change the status, every other field they submit is dropped (field whitelist).
- Duplicate order protection: unique idempotency key on orders, checked in the hook with the database unique constraint as backstop (the portal does not send the key yet).
- Deliveries: one record per shipment or pickup (one per seasonal batch), statuses scheduled / preparing / in transit / delivered, status history, carrier, tracking number, vehicle and driver, proof of delivery upload, delivery fee; quantity allocation and date guards against the parent order (an admin hint shows the kg left to allocate); deliveries sync back to their order.
- Meetings collection (negotiation meetings) linked to orders, created by admins.
- Printable HTML invoice per delivery (A4, localized, right-to-left aware).
- Audit log for orders and deliveries: field-level diff (from / to) of every change, actor (admin / client / system), IP and user agent, written in the same database transaction as the change; entries cannot be edited or deleted.
- Client notifications generated from the same diff when an admin updates an order or a delivery ("Status changed to ...").
- Live preview and drafts / versioning for content.
- PDF invoices (the invoice is HTML which the client prints to PDF)

## Data access, pagination and indexing (checked against the repo)

- Orders list: pagination, sorting, filtering and search are done server-side through the shared `DataTable` component's server mode (manual pagination, sorting and filtering, search debounced 350 ms, skeleton rows while a page loads), so only one page of the signed-in client's orders is fetched at a time (Payload `find` filtered on the client record, newest first). Page-size selector 10 / 20 / 50 / 100. Confirmed by Iheb: this was fixed after an earlier version that fetched up to 100 orders and paginated in the browser (his local repo copy is older and still shows that version). Exact page size, query parameters and relation depth in the new version: TODO, ask if a bullet needs them.
- Delivery-day load (the reactive system that steers clients to lighter days): one Payload query per visible calendar month (`getDailyLoadMap`) that filters in the database on live order statuses and on the date range across the three date fields (express ready date, pre-order ready date, seasonal batch dates), `depth: 0`, then sums kg per day in memory into a day -> load map compared with a daily threshold kept in a CMS global. The calendar refetches on month change and ignores stale responses.
- Lookups that only need an id use `limit: 1` and `depth: 0` (e.g. resolving the Clerk user to its client record).
- Database indexes, via Drizzle / hand-written SQL migrations: partial unique index on the order idempotency key (duplicate-order backstop under concurrent requests), partial unique index for at most one primary address per client, and btree indexes on the delivery-address foreign keys of orders and deliveries (and their version tables).
- Caching: per-page SEO metadata cached with `unstable_cache` and invalidated by tag (see above).

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

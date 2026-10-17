---
id: playpex
name: Playpex
url: https://ihebbelhadj.vercel.app/projects/torrent-streamer
tags:
  [
    nodejs,
    streaming,
    angular,
    react,
    electron,
    frontend,
    backend,
    desktop,
    typescript,
    sqlite,
    networking,
    security,
    auth,
    api,
  ]
stack:
  [
    Node.js,
    Express.js,
    Angular,
    React,
    TypeScript,
    RxJS,
    Electron,
    SQLite,
    Drizzle ORM,
    Better Auth,
    OAuth 2.0 Device Flow,
    OpenAPI,
    WebSocket,
    mDNS / DNS-SD,
    UDP,
    Vite,
    Tailwind CSS,
    shadcn/ui,
    TanStack Query,
    ffmpeg,
    electron-builder,
    GSAP,
    TMDB API,
    Karma,
    Jasmine,
  ]
repo: /home/iheb/projects/Playpex
---

<!-- Raw facts: never rendered. Resume bullets are generated from this text per offer and
     must quote it as their source, so write everything down (scope, team, tools, numbers,
     what you only touched). Keep it true; vague is fine, inflated is not. -->

## Context

- Personal side project, built alone (all commits in the repo are mine, under two accounts).
- Playpex is a self-hosted media server and streaming platform with a "10-foot" TV-style client driven by keyboard / remote through spatial navigation, in the spirit of Plex / Jellyfin.
- Two products: **Playpex Media Server** (a Node.js server installed once on an always-on machine, with a web admin dashboard and a tray app) and **Playpex TV**, its first client (Angular + Electron), talking to the server over a documented, versioned API. Other clients (Android TV, mobile, web) are planned on the same protocol; nothing in the protocol relies on Electron or Chromium.
- Non-commercial personal / educational project.
- First version written Sep 2022 – Jan 2023 (alpha in Sep 2022, v0.9.1 in Oct 2022, backend and frontend integration in Jan 2023); reworked and extended in Oct 2026 (TV series, user profiles, new navigation engine, per-profile watch list and resume, then the split into a media server and separate clients: monorepo, versioned API, LAN discovery, pairing and auth, admin dashboard, desktop server edition).
- Promo video on YouTube: https://www.youtube.com/watch?v=mj4EjDdVXTo
- The first streaming server also exists as a standalone repo, Playpex-backend (https://github.com/IhebBelhadj/Playpex-backend), which provides a ready-to-use streaming API.
- Planned work is listed under "Planned (not built yet)" below; everything else in this file exists in the repo.
- TODO: public repo URL of the main app; whether it has users / downloads.

## Architecture (client / server split)

- Monorepo on npm workspaces (`apps/*`, `packages/*`): `apps/server` (server core), `apps/server-desktop` (desktop server edition), `apps/dashboard` (admin web UI), `apps/tv` (TV client), `packages/protocol` (the API contract shared by server and clients).
- Strict layer separation: one server core with `start()` / `stop()` that never imports Electron, run by thin hosts (a headless CLI entry and an Electron desktop supervisor); the API is the product boundary, so no client depends on server internals; the dashboard is just another client of the server.
- Headless server entry (`apps/server/bin/playpex-server.js`) meant to run under systemd or Docker on Linux boxes / NAS: uncaught exceptions are logged and the process exits with a code so systemd / Docker / the desktop supervisor restarts it. The packaged headless edition (deb/rpm with a `playpex` system user, data in `/var/lib/playpex` and a `playpex-server.service` systemd unit) is planned but deferred (2026-10-16), not built; today a headless machine runs `npm run server` from a clone. TODO: confirm whether I run it myself as a systemd service with my own unit file.
- Designed the boundaries (protocol package, provider registries, repository contracts, thin hosts) so new clients and new providers plug in without touching the core, laying the ground for a plugin-based system.
- Server listens on a fixed port, 28470/TCP (HTTP: API, streams, dashboard), plus 28471/UDP for discovery; both chosen in an IANA range that was never assigned, below the OS ephemeral port ranges and clear of Plex, Jellyfin and other common services.
- If the port is taken by another program, the server starts in a recovery mode (admin dashboard only, on a free loopback port, naming the process that holds the port through ss / lsof / netstat) instead of crashing, so the user can change the port from the dashboard.
- Per-OS data locations for config, cache, downloads and logs (Linux, macOS, Windows), never inside the app, because packaged apps are read-only.
- Server settings in a `settings.json` edited from the dashboard (validated, atomic writes, environment variables override them, secrets masked in the dashboard).
- Structured logging with JSON lines in rotating log files (daily and 10 MB rotation, 7 files) plus an in-memory ring buffer of the last 2 000 entries streamed live to the dashboard; tokens, keys and query strings are never logged.

## LAN service discovery (mDNS / DNS-SD + custom UDP protocol)

- Clients find servers on the local network in two ways and merge the results by the server's id: mDNS / DNS-SD and a custom UDP discovery protocol as a fallback for networks that filter multicast (guest Wi-Fi, some routers, Windows setups). Manual address entry is the third way.
- mDNS / DNS-SD: the server advertises the service type `_playpex._tcp.local` with bonjour-service; SRV record = the HTTP port actually in use; TXT record with the server id, API version, software version and full name; its own host name `playpex-<id>.local` so its A records never clash with the ones Avahi / Bonjour announce.
- Implemented mDNS name conflict probing myself (RFC 6762: 3 queries 250 ms apart) because the library's own probe sent goodbyes for the other server's name; a taken name becomes `<name> (<4 chars of id>)`.
- The server sends an mDNS goodbye (TTL 0) when it stops, so a restart on another port is announced at once and clients follow it.
- Fixed mDNS on machines with several networks (Ethernet + Wi-Fi, VPN, Docker bridges): multicast-dns sends through the default interface only, so queries from another network were answered on the wrong one (found in testing: a Docker container never saw the server); wrote a helper in the protocol package that sends each multicast packet once per network interface, used by the server and the TV client.
- Custom UDP discovery protocol: a client broadcasts the datagram `PLAYPEX_DISCOVER 1` to port 28471 (to 255.255.255.255 and to each interface's directed broadcast address) every 5 s while its server picker is open; each server answers the sender with one JSON datagram (id, name, port, API version range, software version) as its announcement; a server that misses three rounds is dropped.
- The UDP responder only answers senders on loopback, private (RFC 1918), link-local and CGNAT addresses, is rate limited to 20 answers per address per 10 s, and ignores any other datagram.
- Clients store servers by id, never by address: when a saved URL stops answering (DHCP change, new port), discovery finds the same id again at its new address and the stored token stays valid. Every discovered address is confirmed with `GET /api/v1/server` before it is listed.
- Discovery errors never crash the server; their state (mDNS / UDP working or failing) is shown on the dashboard, which warns which method fails and which one still works.
- Firewall: Linux deb packages open the ports with ufw or firewalld when one is active (removed on uninstall); on Windows the tray offers a one-time elevated "Allow through firewall" rule.
- Tested with a discovery test suite (UDP answers, junk ignored, address filter, mDNS records, rename, restart on another port, goodbye) and from a Docker container on a bridge network acting as a second machine (found over mDNS only and over UDP only, followed a server that restarted on another port).

## API and custom protocol

- Versioned REST API under `/api/v1` described by an OpenAPI 3.1 spec in `packages/protocol` (the contract for every client); TypeScript types generated from it with openapi-typescript; spec-first workflow (change the spec, then server and clients).
- Contract test (node:test + ajv) runs a real server and checks every answer against the OpenAPI spec, including the full pairing flow.
- Shared protocol package (CommonJS, no dependencies, loadable by the server, Electron and Angular): API version, ports, discovery constants, error codes, client header helpers.
- Version negotiation through a custom `X-Playpex-Client: <name>/<version>; api=<n>` header; the server answers 426 (CLIENT_TOO_OLD / SERVER_TOO_OLD) outside its supported API version range.
- Uniform error shape `{error, code}` with a fixed list of error codes and statuses; every upstream-backed route always answers the client (502 + JSON error), so a failing external source never leaves the UI hanging.
- Byte-range streaming endpoint (HTTP 206) so playback starts before the download finishes.
- Device leases protocol for streams: each client holds a lease on what it plays, refreshed by a keepalive every 60 s; resources are released 30 s after the last client lets go, idle leases (crashed clients) are reaped after 10 min; server limits (concurrent streams, concurrent transcodes) answer 503 BUSY.
- Client author guide written in `docs/api/` (discovery, pairing, playback, profiles, events, errors and versions), served by every server at `/docs` with the rendered API reference (Scalar) at `/docs/reference`; validated by having a fresh agent sketch a whole client from the docs alone and fixing the gaps it found.
- Network hardening: Host header check against DNS rebinding, CORS allow list, no state-changing GET routes, state-changing requests from foreign web origins refused.

## Authentication (Better Auth + OAuth device flow)

- Auth built on Better Auth with its Drizzle adapter on the server's SQLite database, using its username and device-authorization plugins; public sign-up disabled; Better Auth's endpoints exposed through an allow list only.
- Device pairing follows the OAuth 2.0 device authorization grant (RFC 8628), like linking a TV app: the client shows a code and a QR code, the admin approves it from the dashboard's `/link` page, the tray app or the CLI, the client polls and receives a bearer token. Nothing to type with a remote.
- Device tokens: a year from last use (sliding, renewed at most daily); revoking a device deletes its session and cuts its streams at once (401 PAIRING_REQUIRED).
- Admin auth: username + password (scrypt hashing), HttpOnly signed session cookie, admin sessions limited to 30 days, admin routes refuse device sessions; built-in rate limiting on sign-in (5/min), pairing codes (10/min) and polling.
- Loopback clients (a client on the server machine) are trusted without pairing; ffmpeg's own reads through the API carry a per-process secret.
- Client side (Electron): tokens stay in the main process and never reach the renderer, stored encrypted with Electron safeStorage; the main process injects the Authorization and client headers into every request to the current server (including video and subtitle requests), so no token appears in URLs.
- Profile PINs (4–6 digits, scrypt, lockout after 5 failed attempts) gate user profiles inside the client.

## Real-time feedback on connected clients

- One WebSocket (`ws`) at `/api/v1/events` with topic subscriptions pushes what changes on the server: server status, streaming stats every 2 s, sessions started / updated / ended; the admin also gets live logs, pairing requests and device events. Ping every 30 s, clients reconnect with back-off.
- Dashboard Activity page: every connected client's sessions live (device, title, playback position, play method direct or transcoded, transfer speed), with the option to stop a session; Devices page shows paired devices with online state (socket open or seen in the last 90 s), declared codec capabilities, rename and revoke; live toast when a device asks to pair.
- Tray app status line ("Running · N streams · M devices") and desktop notifications for pairing requests.
- Clients declare their decoding capabilities (containers, video / audio codecs, max resolution) after pairing, so the server can choose direct play or transcoding per device.

## Admin dashboard (React)

- Admin web UI built with React 19, Vite, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, React Router and openapi-fetch on the generated protocol types; served by the server itself, so it works from any machine on the LAN and on headless installs.
- Pages: first-run setup wizard, Overview (addresses, CPU / RAM, traffic, disks, ffmpeg, external provider health), Activity, Devices + `/link` pairing page, Storage, Logs (live, filters, zip download), Settings (tabs, port and directory checks, restart banner), Profiles, About, API docs; dark / light theme from the OS.
- Checked in headless Chrome at desktop (1360 px) and phone (390 px) widths with no console errors.

## Dependencies, installs and bundle size

- npm workspaces: one install and one lockfile at the root, dependencies declared per app; the server's package lists only its runtime dependencies, so packaging copies a small node_modules.
- No native modules to rebuild per platform: SQLite comes from Node's built-in `node:sqlite` (through Drizzle's sqlite-proxy adapter), so the server runs on any Node 24 binary, including the one inside Electron.
- TV client: Angular and its build tools moved to devDependencies (they are bundled into the build output), the app ships only main-process dependencies and no server, torrent or ffmpeg code: an 8.5 MB app archive (asar).
- Dashboard: one ~640 KB bundle; the API docs (react-markdown) and the API reference renderer (Scalar, ~1.9 MB) are lazy-loaded in their own chunks only on their pages, with Scalar's telemetry and external features turned off so nothing leaves the LAN.
- ffmpeg / ffprobe bundled in the desktop server installers from pinned LGPL builds, fetched at build time with SHA-256 checks; analysed the installer size (static builds 142 MB each) and the options to cut it (shared builds, or a custom ffmpeg build with only the codecs used).
- Installers with electron-builder 26: per-user NSIS on Windows (no admin rights), dmg on macOS, AppImage + deb on Linux; auto-updates with electron-updater; designed a release scheme for two products in one repo (tags per product, a channel release per app because electron-updater's GitHub provider reads the repo-wide latest release).
- Desktop server edition: Electron as a windowless supervisor running the same headless server entry in a utilityProcess, with a tray icon (status, pairing approvals, pause, restart, start at login, updates), single instance and crash restarts with back-off.

## Data access layer (SQLite + Drizzle)

- User data in SQLite through Drizzle ORM, schema migrations with drizzle-kit.
- Three layers, each importing only the one below: services (business rules, validation, typed errors) → data access layer (repository contracts with a Drizzle implementation) → database (schema, driver, migrations); so the database driver or engine can be replaced without touching the services.
- Avoided interleaved transactions with an async proxy over a synchronous driver by batching writes in one BEGIN / COMMIT.
- Features on it: profiles (max 8, unique names, optional PIN, kid profiles), watch list, resume points / continue watching (finished at 90 %), watch history, thumbs up / down ratings, and Better Auth's tables plus a devices table.
- Recommendations per profile: seeds from finished views and likes weighted by recency, TMDB recommendations per seed (cached), scored and boosted by genre, excluding already watched titles; kid profiles keep family / animation genres.

## Streaming and playback

- Peer-to-peer (BitTorrent) streaming engine in Node.js: the server listens for byte-range requests, prioritises that range in the download and pumps the downloaded data to the HTML5 video element while it is still downloading. The README describes the streaming as built on media source extensions (MSE).
- Only the file being played is downloaded; the end of the file is prefetched early because MKV files keep their index there, which addresses slow starts.
- On-the-fly audio transcoding with ffmpeg: the player probes each file (ffprobe) and, for audio Chromium cannot decode (Dolby / DTS), plays the server's ffmpeg stream (video copied, audio to AAC) with seeking support.
- Release ranking for playability: prefers playable video codecs and audio Chromium can decode, enough peers, single episodes before season packs, then resolution.
- Pluggable subtitle providers behind one registry (OpenSubtitles, YIFY Subtitles, OpenSubtitles.com, Wyzie Subs); subtitles converted from SRT to WebVTT, legacy code pages decoded, language codes normalized; subtitle references validated so the endpoint is not an open proxy.
- Catalog of movies and TV shows (rows, details, seasons, episodes) from the TMDB API; IMDb ratings of series, seasons and episodes (cached 6 h).

## TV client (Angular + Electron)

- Angular 14 single-page app (TypeScript) packaged in Electron 44, with context isolation, sandbox and a small preload bridge; IPC only from its own window.
- Before the UI loads, the Electron shell resolves the server: the last one used (found again by id), else one on the same machine; otherwise a `/connect` page lists the servers found on the network, offers manual entry and rescan, and runs pairing with the code and a QR code. It can also start an installed but stopped media server.
- Connection error handling: 3 network failures → "Lost connection" (retry rediscovers the server by id), device revoked or incompatible version → back to the server picker with the reason.
- 10-foot TV interface with spatial navigation (navigation with the keyboard / remote) to simulate the TV app experience; Netflix-style "Who's watching?" profile picker, PIN lock per profile, kid profiles, on-screen text keyboard and PIN pad usable with the remote; movie page, TV show page with seasons and episodes, video player with subtitle selection, watch list.
- State management with Angular services and RxJS Subjects / BehaviorSubjects, no NgRx; animations with GSAP timelines.

## Centralized navigation system

- Wrote a new centralized navigation / movement engine (2026) to replace per-page navigation code (six near-copies of the same row logic): shared Angular directives (rows, stacks, grids, sections, items) plus a focus engine service, a scroller and a position store; one keymap defines every key binding (Enter selects, Escape goes back).
- Per-container motion strategy: translated tracks for poster rows, native scrolling elsewhere, so horizontal and vertical mouse scrolling work natively; focus moves by index inside containers instead of on-screen geometry, which was fragile mid-animation.
- Mouse mapped onto the same focus model (hover = focus, click = select, right click = back, wheel = scroll), with no page handling the mouse itself.
- Migrated every page to the engine incrementally (old pages kept working until migrated); patched the vendored js-spatial-navigation library; unit tested with Karma / Jasmine (moves, motion, scroller, position store).

## Testing / tooling

- Server: contract test against the OpenAPI spec and a discovery test suite (node:test + ajv); end-to-end checks in headless Chrome and in Docker / Debian containers (package install, firewall rules).
- TV: Karma / Jasmine unit tests for the movement engine.
- No CI pipeline in the repo yet.
- Verified on Linux; Windows installers built but not run yet, macOS not built.

## Planned (not built yet)

These are designed systems currently in dev:

- **Remote access from outside the home network**: WebRTC connection between client and server, with a server acting as a relay when a direct connection can't be made, and a Redis cache holding the service discovery link maps (which server is reachable where) used to connect a client to its server from outside the LAN. TODO: signaling design, STUN / TURN choice.
- **Encrypted traffic**: HTTPS on the LAN with a self-signed certificate that clients pin at pairing (trust on first use, like SSH): the server creates a key and certificate on first start; TLS served on the same port 28470 by looking at the first byte of each connection (0x16 = TLS handshake), so ports, bookmarks and firewall rules don't change; certificate fingerprint published in the mDNS TXT record, the UDP reply and the server info route; the client pairs over HTTPS and stores the fingerprint with its token, then accepts only that certificate (Electron certificate verify hook); a setting to refuse device tokens and admin sign-in over plain HTTP from the LAN. (Proposal written in the repo's plan.)
- **Certificate rotation**: rotating the server's certificate without forcing devices to pair again. TODO: describe the mechanism (e.g. how clients learn and trust the next certificate).
- **DLNA support**: exposing the server's media to DLNA / UPnP devices (smart TVs, consoles) on the LAN. TODO: details.
- Also on the roadmap in the repo: headless edition (systemd unit, Docker image, one-time setup token), per-device server-side playback decision (direct play vs transcode from declared capabilities), catalog calls moved behind the server, a TypeScript client SDK, Android TV / mobile / web clients, phone remote.

## Known limits (honest)

- Chromium cannot decode Dolby / DTS audio; handled by server-side audio transcoding when ffmpeg is available, else the player warns when there is no sound. No video transcoding yet.
- LAN traffic is plain HTTP today (see the planned encryption above); access from outside the LAN is not supported yet.
- Trailers through youtubei.js are limited by YouTube's proof-of-origin checks.
- Phone remote: only a stub exists in this repo. TODO: was the Ionic mobile controller built somewhere else (other repo)? The README listed it as a future update.

## From past resumes

- Torrent streamer in Node.js with backend wrapper using MSE API for seamless browser playback. Angular frontend, Electron desktop app to bundle the engine and the frontend, and Ionic mobile controller.
  - Torrent streamer in Node.js with backend wrapper using MSE API for seamless browser playback. Angular frontend, Electron desktop app, and Ionic mobile controller.

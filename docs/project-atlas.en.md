# Projects and how to use them

[中文](project-atlas.md) · **English** · [Bilingual profile](../README.md) · [English profile](../README.en.md)

This guide covers the problems, audiences, features, technology, entry points and engineering lessons behind my public projects. The baseline review on **3 November 2026** covered 12 public repositories: eight product projects, three upstream forks and this profile. This is a dated review scope, not a current inventory of the account. AgentCompare notes were updated from current public documentation on 9 November 2026. AirStudy's implementation notes also draw on a local engineering review; its public repository does not contain the complete application.

| Project | Purpose | Main technology |
| :--- | :--- | :--- |
| [job_radar](#job-radar) | Search traceable Chinese recruitment data locally | Python, SQLite, CLI, MCP, GitHub Actions |
| [QGauss AI](#qgauss) | A self-hosted multimodal creative workspace | TypeScript, Vue, NestJS, Prisma, SQLite |
| [AgentCompare](#agent-compare) | Compare answers, files and live pages in DSH | TypeScript, React, Git worktree, DSH |
| [BugGPS](#bug-gps) | Record a browser bug and verify its fix by replay | JavaScript, Playwright, Git, DSH |
| [skill-healthcheck](#skill-healthcheck) | Diagnose skills that silently stopped working | TypeScript, Git, YAML, local session evidence |
| [unremember](#unremember) | Selective, reversible forgetting for local agents | TypeScript, JSONL, Zstandard, SHA-256 |
| [Xiangcun Xiaozhao](#xiangcun) | Connect restaurant ordering, kitchen and accounting workflows | React, TypeScript, Hono, SQLite, SSE |
| [AirStudy](#airstudy) | An Android focus experience structured as a flight | Kotlin, View/XML, Room, Hilt, DataStore, Ktor |

<a id="job-radar"></a>

## job_radar

**Problem and audience.** Chinese campus, internship and experienced-hire opportunities are spread across many sources. Applicants, analysts and agent users need to search them while retaining the original text, eligibility evidence and observation dates.

**What it does.** Python adapters normalize public recruitment sources into SQLite snapshots for structured jobs, full descriptions and recruitment calendars. GitHub Actions collects data; Releases distribute compatible snapshots. CLI, MCP and Skill integrations share query rules. Filters include companies, city unions and exclusions, recruitment type, graduation year and literal text search, alongside changes and calendar queries.

```bash
pip install "jobsearchradar[mcp]"
jobradar update
jobradar search --city 北京 --type intern --table
jobradar doctor
```

Use `jobradar show <job_id>` for a listing's details and `jobradar calendar --table` for calendars. MCP clients can run the stdio command `jobradar-mcp`. Company names and source job text may remain Chinese: an English guide does not imply translated source data or semantic matching.

**Engineering lessons.** Failed collection must not mark jobs as closed. Graduation years require explicit evidence; unknown eligibility stays unknown. Listing freshness and description freshness are tracked separately. Official and aggregator coverage use separate categories and a fixed target pool. Shared query behavior and compatible exports matter as much as collection scale.

**Scope.** Snapshots can lag the original sites. Configuration counts do not equal current openings, and recruitment notices do not always represent individual roles. Check the source before applying. [Repository and current instructions](https://github.com/lijiaqi-AI-Product-Manager/job_radar) · [Detailed Chinese notes](projects/job-radar.md)

<a id="qgauss"></a>

## QGauss AI

**Problem and audience.** Individual creators and small AI site operators often have separate tools for chat, visual work and administration. QGauss brings these workflows into one self-hosted workspace.

**What it does.** Vue, Pinia and Rollup power the client; NestJS, TypeScript, Prisma and SQLite support the backend. Capabilities include multi-model streaming chat, attachments, branching, web search, image creation and selection editing, video, voice history and playback, mind maps, custom applications and extension canvases. Operations tools cover accounts, model channels, entitlements, memberships, orders, email receipts and encrypted backups.

After cloning the repository:

```bash
npm ci
npm run setup:guided
npm run serve:prod
```

Open `http://127.0.0.1:9520/setup`, use the local installation credential to create the first administrator, then configure model channels and site settings. Production setup is separate from the development path with simulated providers and demo accounts.

**Engineering lessons.** Request acceptance, allowance reservation, saved output and final settlement need durable phases so retries, cancellation and restarts do not charge twice. SQLite transaction scheduling avoids tying up execution threads while waiting for locks. Account changes invalidate late responses. Reusing artwork, transferring image selections and recovering extension requests must preserve the original operation and avoid accidental new generation.

**Scope.** Database, scheduling and recovery have been validated for a single-instance setup. Real model quality, email delivery, merchant payments, production load and off-machine recovery require their own deployment checks. [Repository and setup](https://github.com/lijiaqi-AI-Product-Manager/QGauss-AI) · [Detailed Chinese notes](projects/qgauss.md)

<a id="agent-compare"></a>

## AgentCompare

**Problem and audience.** Developers, product builders and designers need to compare answers and implementations under the same task, inspect the results and choose what to keep.

**What it does.** This DeepSeek Harness plugin compares 2–4 answers, files or runnable web pages in the main conversation. Set models and styles, compare blind or openly, then review changes before adopting or saving a result. TypeScript and React connect settings, isolated candidates, live previews and conversation memory. A Git project starts candidates from a shared baseline; a plain folder can start empty and save the choice into a new subfolder.

**Getting started.** Install dsh-agent-compare through the DSH Desktop Plugins page, or follow the [Web-profile instructions](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare/blob/main/README.en.md#install). Click A|B in the composer, choose the number of versions and comparison settings, and send a task. Read answers and files or try the pages before choosing; inspect the target and changes before confirming adoption.

**Engineering lessons.** The initial source review covered shared baselines, bound acceptance files, concurrent edits, adoption rehearsal, persistent recovery records and ownership-checked cleanup. Current features also keep comparison results in the owning conversation and allow an explicit choice of shared context. Model output quality and runtime support still need their own evidence.

**Scope.** Current documentation covers answers and files from any folder, plus Vite, Node and static-site previews in Git roots or subfolders. Content comparison does not establish arbitrary-language execution or functional coverage. Login, shared backends and external databases need separate validation; host isolation has platform-specific limits. Feature notes updated from public documentation on 9 November 2026; the engineering history retains its earlier review basis. [Repository](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare) · [Detailed Chinese notes](projects/agent-compare.md)

<a id="bug-gps"></a>

## BugGPS

**Problem and audience.** A verbal bug report can be difficult to reproduce, and an agent saying “fixed” is insufficient evidence. BugGPS helps developers, testers and people reporting browser interaction problems preserve the original expectation.

**What it does.** JavaScript, Playwright, Git snapshots and DSH tools record actions, expected results, optional checkpoints and essential steps. Locking requires repeated failure with a consistent signature. Verification starts the application from the current workspace and replays the complete scenario, continuing to observe checks after the final action. Case hashes and write protection preserve the recorded contract.

After installing the local checkout in a DSH profile, try:

```bash
node bin/buggps.js demo ../buggps-demo
node bin/buggps.js doctor --repo ../buggps-demo
```

Record the bug and mark the expected behavior, lock the failure, let the agent edit the application, then verify. Configure a separate local serve command and address in `buggps.config.json`.

**Engineering lessons.** Passing against another server does not bind a result to the current patch. Removing a feature, disabling a control, delaying an error or drifting to a fuzzy locator can produce misleading success. Checkpoints, positive expectations, repeated replay and observation windows address these counterexamples. Secret fields store references rather than their values.

**Scope.** `VERIFIED` covers the recorded scenario only. Validated use centers on Chromium-based browsers, React/Vite, resettable front-end state and DOM assertions. Dragging, arbitrary global keyboard actions and workflows that mutate backend data are not covered by this claim. [Repository and installation](https://github.com/lijiaqi-AI-Product-Manager/dsh-bug-gps) · [Detailed Chinese notes](projects/bug-gps.md)

<a id="skill-healthcheck"></a>

## skill-healthcheck

**Problem and audience.** Claude Code, Codex and DSH users can have skills that remain on disk but stop triggering after upstream descriptions, loading rules or local precedence change.

**What it does.** A TypeScript CLI combines host-specific discovery and parsing rules, upstream Git changes and local session evidence. It reports changed names, descriptions, scripts and loading behavior, then uses timelines and deterministic rules to rank plausible explanations. It does not automatically update source skills.

```bash
npx skill-healthcheck
npx skill-healthcheck ls
npx skill-healthcheck why "Why did it stop answering in Chinese?"
```

Use `--offline` for local checks, `--no-sessions` to skip session analysis and `--json` for automation. `adopt --repo <source-repository>` can register provenance for copied skills. A companion DSH plugin records snapshots and exposes chat commands.

**Engineering lessons.** Host parsers and precedence cannot be treated as interchangeable. Authentication failures, unreadable caches and failed blob reads must not be reported as deletions. A description edited after a skill stopped being used cannot explain the earlier change. Source matching, Windows path identity, CRLF handling and strict optional explanation payloads avoid incorrect conclusions or unintended disclosure.

**Scope.** `why` ranks suspects rather than proving causation. Loading successfully does not guarantee model invocation. Optional model-based explanations send relevant skill changes; default deterministic checks do not call a model. [Repository and installation](https://github.com/lijiaqi-AI-Product-Manager/skill-healthcheck) · [Detailed Chinese notes](projects/skill-healthcheck.md)

<a id="unremember"></a>

## unremember

**Problem and audience.** Deleting one visible message may leave the same content in local summaries, memories, histories and caches. Claude Code and DSH users need selective removal while preserving other context and a way to recover.

**What it does.** TypeScript and Node built-ins process supported JSONL and Zstandard stores. The workflow is **plan → inspect → back up → apply → probe a fork → roll back if needed**. Plans simulate removal and scan residuals. Applying checks file hashes, allowed paths and session liveness before backups and atomic writes. Optional backup encryption uses AES-256-GCM.

```bash
npm install -g unremember
unremember sessions
unremember plan last --text "content to remove"
```

Inspect the plan, then use `apply <plan-id> --yes`. Verify on a fork with `verify <session> --canary <target>`; restore with `rollback <plan-id>`. End the target session first: changing files cannot replace context already loaded by a running agent.

**Engineering lessons.** Cleanup must preserve parent references, tool pairs, DSH sequence numbers and compressed frame layout. Empty or inconclusive verification answers are not success. Plans must avoid retaining plaintext previews. Path validation, plan locks, file-change checks and explicit recovery errors protect concurrent or interrupted operations.

**Scope.** This handles supported local agent files, not cloud retention, model weights, other devices or repository history. Fork probes are bounded leak checks, not proof of universal semantic forgetting. No Codex file adapter is included. Optional semantic matching requires a configured endpoint and sends relevant excerpts to that endpoint. [Repository and installation](https://github.com/lijiaqi-AI-Product-Manager/unremember) · [Detailed Chinese notes](projects/unremember.md)

<a id="xiangcun"></a>

## Xiangcun Xiaozhao

**Problem and audience.** Independent restaurants need customer ordering, kitchen operations, stored-value accounts and financial records to follow consistent rules. Brand configuration makes the code reusable beyond one restaurant.

**What it does.** React/TypeScript clients connect to a Hono and SQLite backend, with shared Zod contracts and SSE order updates. Workflows include QR table ordering, modifiers, additional dishes, pickup progress, owner order management, stored-value balances, refunds, reconciliation, history, overnight closing reports, shift reports and receipt or label printing.

**Getting started.** Configure a brand and a separate administrator password, run `npm ci`, then start `npm run dev:server`, `npm run dev:customer` and `npm run dev:admin` in separate terminals. The customer development entry is `http://localhost:5173/?table=12`; the owner interface is `http://localhost:5174`.

**Engineering lessons.** Additional dishes become child orders so original prices and ledgers remain intact. Idempotency checks precede validations that would otherwise reject a successful retry after the cart has been cleared. Closing reports follow the store's overnight business shift. One image upload produces coordinated full-size and thumbnail assets. Printing requires concrete paper, encoding, cutter and connection settings, including local USB and label paths.

**Scope.** Cash and external wallets may be recorded as counter payments; this does not imply an integrated online acquiring gateway. Stored-value deductions are internal ledger operations. Stock quantities and full loyalty tier benefits are not inferred from the interface. Physical devices and production environments need their own checks. [Repository](https://github.com/lijiaqi-AI-Product-Manager/xiangcunxiaozao) · [Detailed Chinese notes](projects/xiangcun.md)

<a id="airstudy"></a>

## AirStudy

**Problem and audience.** AirStudy explores a more tangible focus experience for Android users by organizing time around airports, routes, preparation, sessions, boarding passes and flight history.

**Technology and engineering.** The local implementation uses Kotlin, View/XML, Hilt, Room, DataStore, a multi-module Gradle structure and a Ktor server. Important problems include foreground services, background retries, session identity, process recovery, account switching, database migrations and keeping planned origins synchronized across screens.

**Entry and scope.** The public [development branch](https://github.com/lijiaqi-AI-Product-Manager/AirStudy/tree/work/single-flight-integration) contains the Android project, a server directory and [build instructions](https://github.com/lijiaqi-AI-Product-Manager/AirStudy/blob/work/single-flight-integration/docs/development.md). Its README describes implemented flight and local-record workflows alongside remaining work on cloud updates, maps, statistics and device layouts. Development source is not a released app or evidence of full device acceptance. Engineering history here comes from the 3 November 2026 local review; the public entry was checked on 9 November. Follow the branch for current scope. [Detailed Chinese notes](projects/airstudy.md)

<a id="upstream"></a>

## Upstream forks and attribution

The following repositories are forks. Their original development and historical fixes belong to their upstream authors; they are not presented as my original products or contributions.

| Fork | What I studied | Upstream |
| :--- | :--- | :--- |
| [lobe-chat](https://github.com/lijiaqi-AI-Product-Manager/lobe-chat) | Next.js/React/TypeScript workspace design; model runtimes, knowledge files, branching, tools, desktop bridges and database layers | [LobeHub](https://github.com/lobehub/lobehub) |
| [coai](https://github.com/lijiaqi-AI-Product-Manager/coai) | Go, React, MySQL and Redis; provider routing, channel priorities, subscriptions, quotas, chat and administration | [CoAI](https://github.com/coaidev/coai) |
| [blob-service](https://github.com/lijiaqi-AI-Product-Manager/blob-service) | Python/FastAPI file processing; MarkItDown, format handlers, OCR, speech and storage adapters | [Blob Service](https://github.com/coaidev/blob-service) |

Follow each upstream's current deployment instructions and license. OCR, speech, storage and provider-dependent capabilities require their respective configuration. Commercial-edition claims do not automatically describe community code. [Detailed Chinese reading notes](projects/ecosystem.md)

## This profile and related experience

The [profile repository](https://github.com/lijiaqi-AI-Product-Manager/lijiaqi-AI-Product-Manager) contains a bilingual home page, an English-only overview, original theme-aware SVG artwork, project guides and experience summaries. Public source references are recorded in [the review index](review-sources.json).

MUNity, the travel agent prototype and personal multi-agent research workflows are described from my résumé, rather than a public code review. Read [experience](experience.en.md) for their context.

[Back to the bilingual profile](../README.md) · [English profile](../README.en.md) · [中文项目档案](project-atlas.md)

---
name: performance-digest
description: >
  Pulls real organic social performance data (Facebook/Instagram engagement, via a direct Meta connector when one is available) and ranks content by performance, cross-references it against what was actually published (Business/[slug]/social/content-calendar.md), and produces a performance digest. Every run also writes the measured numbers back into that calendar (Performance and Verdict columns, plus a per-format benchmarks block), so history accumulates instead of living in old chat threads. On request it also builds a branded HTML dashboard. Reads Business/[slug]/context/ at runtime rather than hardcoding any data connector. Use for weekly/monthly recaps, "how did our posts do" questions, or before planning the next content batch. Does NOT pull paid ad metrics (spend, CPC, ROAS) — say so plainly rather than estimating.
---

# Performance Digest

Turn real, pulled data into a digest of what worked, what didn't, and what that implies for the next batch of content — plus, when asked, a dashboard someone can actually open and look at again. This skill doesn't originate content and doesn't plan campaigns; for those, see `campaign-plan` and the content skills.

---

## Workspace and file access — resolve this before any read or write

Every `Business/...`, `memory.md`, and other workspace path in this skill is relative to your workspace root. Resolve it **once** at the start of the run, then use the same method for every read and write that follows:

1. **The current project folder is the workspace root.** If a folder is open or mounted in this session, that folder is the root. This is the default and needs no configuration.
2. **`aimm-config.md` at that root can override it.** If it sets `workspace_root`, use that path instead. If it sets `storage_mode: dropbox`, read and write through the Dropbox MCP tools (`list_folder`, `fetch`, `create_file`, `delete`) at that path. Dropbox is used only when the config says so, and only at the path the config gives — never a built-in one.
3. **Nothing reachable.** Say so in one line and ask which folder to use, then work from what you're told in chat. Never invent a workspace path or brand context, and never quietly produce generic content as if context had been read.

A failed read is **not** proof a file is missing. Retry, or list the parent folder, before reporting anything absent — especially before saying a business profile doesn't exist.

**Before falling back to a lesser path,** check `.aimm/environment.md` for what `doctor` last found. Treat it as a hint, not proof — if it is stale or absent, probe and proceed. The live probe is always authoritative.

**Plugin-relative paths are the exception.** Paths beginning `assets/`, `scripts/`, `library/`, or `references/` live inside this skill's own folder in the installed plugin — *not* in the workspace root and *not* in Dropbox. Read those from the skill directory on every surface, mobile included, and never look for them through a connector.

**Writing in Dropbox mode:** Dropbox cannot append or edit in place. Fetch the file's live content immediately before changing it, then delete and recreate it at the same path. Never write from an earlier read.

**One business per workspace.** The active slug comes from `aimm-config.md` (`business:`), or the single folder under `Business/` that isn't `_template`. If several exist and the config is silent, ask once. Never mix two businesses' content.

---

## 1. Read the business context

The active business is already resolved. Before pulling anything:

0. **Confirm the business profile.** The active business was resolved once at the top of this skill — don't re-resolve or re-ask here. If no profile exists yet, stop and run `business-setup` rather than writing against an empty context folder.
1. Read `Business/[slug]/context/brand-voice.md` — content pillars and hook framework, used later to explain *why* something performed.
2. Read `Business/[slug]/context/audience.md` — for framing results in terms of real audience segments, not generic language.
3. Read `Business/[slug]/context/style-guides/social.md` — documented cadence and content-pillar rotation, used to group results by pillar.
4. Read `Business/[slug]/context/style-guides/ads.md` — to note whether paid is supposed to be active for your business. This does NOT mean paid data can be pulled (see Section 2) — it only tells you whether to flag "paid is active per your own strategy, but this environment can't report on it" versus "paid isn't active, so its absence is expected."
5. Read `Business/[slug]/social/content-calendar.md` — the record of what this project has actually published for your business (date, format, channel, file). This is your cross-reference for matching a high/low performer back to its content pillar, format, and the actual copy that was posted (via the `File` column pointing into `Business/[slug]/examples/`).

**If `Business/[slug]/context/` is incomplete,** say so and proceed with whatever real information exists — don't invent a content-pillar rotation or cadence that isn't documented.

---

## 2. Data sources — check what's actually available before promising anything

**Do this check every time, out loud in your output, before pulling anything.** This is not optional scaffolding — connector availability varies per business and per session, and inventing numbers when a connector isn't available would be a serious failure mode.

The core data this skill needs is Facebook/Instagram post-level and account-level engagement. **A direct Meta (Facebook/Instagram Graph API) connector is the path**, and the only one.

### 2a. Check whether a Meta connector is actually connected

Find it by capability, not by name — search for a Facebook/Instagram insights tool (posts, page insights, account insights). **Connector prefixes differ between installs, so never match a literal `mcp__…` string**, and check before assuming absence: availability changes session to session.

If one resolves, pull posts and account insights for the resolved period. If none resolves, go to Section 2b — that is a normal outcome, not an error.

### 2b. Fallback when live platform data isn't available

`Business/[slug]/social/content-calendar.md` and `Business/[slug]/examples/` tell you what was *published*, not how it *performed* — there is no engagement data in them. When no Meta connector resolves, say clearly that this digest can only report **publishing activity** (what went out, when, on what pillar) rather than **performance** (how it did), and ask whether the user can supply an export or screenshot from the platform's own insights.

**Leave the Performance and Verdict columns empty. Never write a zero.** A missing metric and a measured zero mean opposite things, and a zero written today becomes a false data point in every median from here on.

### 2c. Paid ad metrics — structurally unavailable, every time, for every business

**There is no Meta Ads / paid-ads connector in this environment.** Spend, CPC, CPL, ROAS, frequency — none of it is pullable, regardless of whether `style-guides/ads.md` says paid is active for your business. State this plainly in every digest's caveat section rather than estimating or letting the absence go unremarked.

---

## 3. Inputs

1. **Period** — default to the last 7 days if not given. Accept relative ("this week," "last month") or absolute phrasing.
2. **Platform focus** (optional) — default to both/all connected platforms.
3. **Depth** (optional) — quick digest (top/bottom 3) vs. full digest (every post ranked). Default: quick.

Resolve the period into concrete since/until dates. Cap `until` at today.

---

## 4. Workflow

1. Run the Section 2 availability check and state the result before pulling data — including which path (Meta direct, or the publishing-activity fallback) was actually used.
2. Pull post-level and account-level data per Section 2a for the resolved period.
3. **Rank posts** by engagement: `likes + comments` at minimum; prefer `(likes + comments) / reach` when reach is available, so a low-reach post doesn't look artificially strong. Identify top 3 and bottom 3 (excluding posts under 48 hours old from the "bottom" list — they haven't had time to accumulate engagement).
4. **Cross-reference** each top/bottom post against `Business/[slug]/social/content-calendar.md` by date/channel to identify its content pillar and format, and pull the actual copy from the linked file in `Business/[slug]/examples/` if useful context for explaining *why* it performed. If a post isn't found in the calendar (published outside this system, or before it existed), say so rather than guessing at its pillar.
6. **Identify patterns** — group top/bottom performers by content pillar, format, and hook style (per `brand-voice.md`'s hook framework). State patterns as hypotheses, not certainties — organic sample sizes are usually small.
7. **Write the numbers back into the content calendar** — see Section 5. This is not optional and not a "if the user asks" step. A digest that only produces a report leaves the calendar a write-only log, and every future run starts from zero again.

---

## 5. Write the numbers back into the content calendar

The digest is a snapshot. The calendar is the record. **Every run writes measured numbers back into `Business/[slug]/social/content-calendar.md`**, so the business's own history accumulates instead of living in old chat threads.

### 5a. Calendar schema

Two columns beyond the base row:

`| Date | Format | Channel | Summary | Status | Performance | Verdict | File |`

**Performance** — a single packed, human-readable string of only what was actually measured, followed by the measurement date:

`reach 263 · views 338 · saves 0 · int 16 · ER 6.1% (m. 08-12)`

- Include a metric only if the platform returned it. **Never write a zero for a metric that failed to fetch** — omit it. A missing metric and a measured zero mean opposite things.
- `ER` is `total_interactions / reach`, one decimal. Only compute it when both were measured.
- `(m. MM-DD)` is the measurement date, and it matters: reach keeps accruing, so a number is only meaningful alongside when it was read.

**Verdict** — one of `Win`, `Average`, `Under`, `Too early`, or `—`:

- `Too early` — post is under 48 hours old. Never judge one before then.
- `—` — not measured, or the connector couldn't return reach.
- Otherwise compare against **your business's own rolling median for that same format** (Section 5b), never an absolute threshold or a cross-client number:
  - `Win` — reach ≥ 1.25× the format median **and** ER at or above the format median
  - `Under` — reach ≤ 0.75× the format median, **or** ER below half the format median
  - `Average` — everything else

A Reel doing 263 reach is not comparable to a static post doing 47, and neither is comparable to another business. Judging a format against its own baseline is the whole point — otherwise every static post reads as a failure and every Reel as a win, which tells you nothing you didn't already know.

### 5b. Maintain the benchmarks block

Keep a short block at the top of `content-calendar.md`, directly under the intro, and update it on every run:

```
## Benchmarks (updated YYYY-MM-DD)

| Format | Posts measured | Median reach | Median ER |
|---|---|---|---|
| Reel / video | 4 | 231 | 4.8% |
| Single image | 2 | 52 | 3.9% |
| Carousel | 0 | — | — |
```

Use the **median**, not the mean — one outlier post otherwise moves the bar for everything. Include the sample size on every row, and when a format has **fewer than 4 measured posts, write the verdict as `Average` regardless** and note the block is provisional. Three posts is not a baseline.

### 5c. Write-back rules

- **Only measured numbers.** No estimates, no interpolation, no "approximately." If a metric didn't come back, it isn't in the string.
- **Reach only grows.** If a re-measurement returns a *lower* reach than what's already recorded, do not overwrite it — flag it in the digest as a likely API inconsistency and leave the higher figure with its original date.
- **Re-measure at 7 and 30 days.** A post measured at 24 hours is a partial read. When a run's period covers posts already carrying a `(m. …)` stamp older than a week, refresh them and update the date.
- **Rows for posts published outside this system** still get performance written back; mark Summary as `Not produced by this system` rather than skipping the row, or the benchmarks skew toward only what the system made.
- **Match rows by content, not by date alone.** Calendar rows are often dated by the day a piece was *created*, not published — three Reels can all log as `2026-08-05` but go live on 08-06, 08-07, and 08-08. Date-only matching silently skips them and the benchmarks quietly skew. Match on project/topic name, then confirm with the date. Where the two differ, append `pub. MM-DD` to the Performance string so the gap is visible.
- Dropbox has no in-place append — fetch the live file immediately before editing, then delete and recreate at the same path. Never write from an earlier read.

### 5d. What this unlocks

Once two or three runs have accumulated, the calendar answers questions no single digest can: which formats hold up over months, whether a hook pattern repeats its result, and which specific post is worth spinning variants from. Any skill that needs "what actually worked" reads this file rather than re-pulling the API.

---

## 6. Output — the digest (Mode A, default)

### Summary
Period covered, one line confirming this is an **organic engagement digest** (never implying paid data is included), and a one-line note on overall trend if determinable.

### Top Performers / Bottom Performers
| Post | Platform | Date | Pillar/Format | Engagement | Likely Driver |
|---|---|---|---|---|---|

### Patterns Observed
2-4 bullet hypotheses tying top/bottom performers to content pillars and hook types.

### Recommendations
What to repeat, what to retire, any content-pillar gaps noticed (e.g. a pillar that hasn't run in a while).

### Data Availability
State plainly, every time: which data path was actually live for this run (Meta direct, or the fallback per Section 2), what fell back to publishing-activity-only, and that paid metrics are out of scope in this environment (2c). This section is not optional boilerplate — it's the difference between a real digest and a fabricated one.

---

## 7. Output — dashboard artifact (Mode B, on request only)

This is a secondary output — build it when the user asks for a dashboard/visual version, not automatically with every digest.

Reference: a prior dashboard build is worth learning from — tabbed layout (Overview / Instagram / Facebook / Insights), date-range navigation, print-to-PDF via the browser print dialog. Its own `CLAUDE.md`/`DEBUGGING-NOTES.md` document real fragility worth avoiding here: large `callMcpTool` responses (~800KB+) can hang the artifact sandbox indefinitely, access tokens expire (~60 days) and need manual refresh, and a live in-artifact "Refresh" button that calls MCP tools at view-time is a known-fragile pattern — that project's own Refresh is documented as unconfirmed working.

Default to a **static snapshot dashboard**, not a live-refreshing one: build a single self-contained HTML file seeded with the data already pulled and ranked in Mode A above, styled using `Business/[slug]/context/brand-board.md` (colors, fonts, logo treatment). Include the same tabs/sections pattern (Overview, per-platform breakdown, top/bottom performers, patterns/recommendations) and a print-to-PDF affordance (`window.print()` on a button, with print-specific CSS). To refresh with new data, re-run this skill for a new period and regenerate — don't build live `window.cowork.callMcpTool()` refresh logic unless the user explicitly asks for it and accepts the known fragility above; if they do, keep responses under the ~800KB range that's documented to hang the sandbox (never fetch `include_images: true` or embed full-size media).

**Delivering the dashboard.** Write the `.html` to `Business/[slug]/examples/` alongside the digest, using the same filename stem, and state its full path. Confirm the write before you report it — never report a path you did not verify. Rendering or attaching it in the conversation is a surface-dependent extra: do it after the file is written if this surface supports it, and say nothing about it if it doesn't. Do not call a tool to hand the file over, or to add it to any gallery, unless you have confirmed that tool exists in this session; assume none does.

The digest itself (Mode A) is plain text and is the part that matters; never skip or delay it because the dashboard can't render.

---

## 8. Save Your Output

Once the digest (Mode A) is finished, save it automatically — don't ask first.

Save the full digest to `Business/[slug]/examples/` as `YYYY-MM-DD_performance-digest_[period-slug].md` (e.g. `2026-07-09_performance-digest_last-7-days.md`). If a Mode B dashboard was also built, note its delivery in the digest file rather than duplicating the dashboard's own persistence — the dashboard is persisted via the artifact system (Section 6), not saved into `Business/[slug]/visuals/`, since that folder is `graphic-production-studio`'s alone (see `_skills/README.md`).

---

## 9. Quality bar

- The Data Availability section is never skipped and never glosses over a connector that wasn't actually live.
- Never fabricate a CPC/spend/ROAS number — say the data doesn't exist in this environment.
- Patterns are stated as hypotheses given small organic sample sizes, not as proven causes.
- Measured numbers were written back into the content calendar and the benchmarks block was updated — a run that only produced a report is an incomplete run.
- No metric was recorded as `0` when it actually failed to fetch.
- Verdicts were set against your business's own per-format medians, never absolute thresholds or another business's numbers.
- If `Business/[slug]/social/content-calendar.md` doesn't cover the full period (e.g. a new business profile, or a period before this system existed), say so rather than silently under-reporting.

## 10. Response behavior

**If the business isn't clear:** ask before pulling anything.

**If a data source isn't available:** say so plainly per Section 2, and offer the fallback (publishing-activity-only digest, or ask for a manual export) rather than quietly producing a thinner report without explanation.

**After the digest is saved:** confirm the save with its file path **and the number of calendar rows updated**, then ask: "Want me to draft the next batch of content leaning into what's working (hands off to the relevant content skill), run `brand-review` on the bottom performers to check whether voice — not just topic — was the issue, build this into a branded dashboard artifact, or pull a longer historical window to confirm these patterns aren't a one-week fluke?"

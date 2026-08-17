---
name: campaign-plan
description: >
  Generates a full marketing campaign brief — objectives, audience, key messages, channel strategy, week-by-week content calendar, asset list, success metrics, budget, risks — coordinating multiple skills into one plan instead of one-off assets. Reads brand voice, audience, products, and channel status from your Business/[slug]/context/ folder at runtime rather than hardcoding any channels or budget. Use when the user asks to plan a campaign, a seasonal push, a lead-gen sprint, a launch, or a content calendar — anything needing multiple content pieces coordinated toward one goal rather than a single post or ad. For a single piece of content, use the relevant content skill directly instead.
---

# Campaign Plan

A campaign is more than a pile of individual posts and ads pointed at the same rough goal — it's a plan where every piece reinforces the same message, on a timeline, with a way to tell afterward whether it worked. This skill produces that plan. It doesn't write the individual pieces itself — it maps out what's needed and hands off to the content skills that actually produce each one.

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

The active business is already resolved. Before doing anything else:

0. **Confirm the business profile.** The active business was resolved once at the top of this skill — don't re-resolve or re-ask here. If no profile exists yet, stop and run `business-setup` rather than writing against an empty context folder.

1. Read `Business/[slug]/context/brand-voice.md` — positioning, messaging framework, CTA toolkit.
2. Read `Business/[slug]/context/audience.md` — segments, pain points, decision triggers.
3. Read `Business/[slug]/context/products.md` — real offers, funnel, and any honesty flags (pre-revenue/pre-case-study businesses need metrics and proof-point sections handled differently — see Section 5 and 7).
4. Read `Business/[slug]/context/brand-board.md` for visual system reference (used when listing creative assets needed, not for writing copy here).
5. Read the relevant `Business/[slug]/context/style-guides/` files — `social.md` and `ads.md` are almost always relevant; `blog.md`, `lead-magnets.md`, and `email-newsletter.md` depend on which channels the campaign will use. **Check `ads.md` specifically for whether paid is even an active channel for your business** — don't build a Meta ad budget line into a campaign for a business whose own strategy says organic-only.
6. Also read `Business/[slug]/social/content-calendar.md` before proposing a new campaign calendar, so the proposed week-by-week plan doesn't overlap or conflict with what's already scheduled or published for your business.
7. Also check `Business/[slug]/examples/` for prior campaign briefs (content-type `campaign-brief`) as a reference for what's already been proposed or run for your business.

**If `Business/[slug]/context/` is incomplete,** say so, and build the plan on whatever real information exists rather than inventing budget figures, historical benchmarks, or channel commitments that aren't documented anywhere.

---

## 2. Inputs

Gather the following. If not provided, ask before proceeding:

1. **Campaign goal** — the primary objective (e.g. drive bookings/consultations, a seasonal push, awareness for a specific offer, a 30-day content calendar sprint, a retargeting push for warm leads). Should map to something real in `products.md`'s funnel.
2. **Timeline** — duration and any fixed dates.
3. **Budget** — total campaign budget, or confirmation this is organic-only (check `style-guides/ads.md` first — don't ask if the answer is already documented there).
4. **Additional context** (optional) — a specific offer/service to promote, a seasonal opportunity, existing content/proof to feature.

---

## 3. Campaign brief structure

### 1. Campaign overview
Campaign name, one-sentence summary, primary objective with a specific measurable goal, secondary objectives.

### 2. Target audience
Pull directly from `Business/[slug]/context/audience.md` — primary segment, any secondary segments relevant to this campaign, pain points and decision triggers this specific campaign should speak to. Don't invent demographic/psychographic detail that isn't in that file — if it's thin, say so.

### 3. Key messages
**Core campaign message** (one sentence, specific to this campaign's goal).
**Supporting messages** — pulled from `brand-voice.md`'s messaging framework and hook patterns, adapted to this campaign's angle.
**Proof points** — pulled from real material in `products.md`. If the business is flagged pre-revenue/pre-case-study, this section leans on process transparency and founder credibility rather than invented results — flag this explicitly rather than quietly working around the gap.

### 4. Channel strategy
Build only across channels that are actually real for your business:

- **Paid (Meta or other)** — only if `style-guides/ads.md` confirms this is an active channel. If it is, split by objective (lead-gen / retargeting / awareness) per `ad-creative-brief`'s framework, with budget percentages. If paid isn't active, state that plainly and skip this section rather than defaulting to a generic ad plan.
- **Organic social** — per `style-guides/social.md`'s documented platform priority, posting cadence, and content pillars. Map each week's posts to a pillar rotation instead of assigning content arbitrarily.
- **Email / newsletter** — per `style-guides/email-newsletter.md`, if your business has an active list/tooling; note the gap if they don't (many early-stage businesses won't yet — see their documented gap as an example of how to note this honestly).
- **Blog / organic search** — per `style-guides/blog.md`, if the campaign includes an SEO/content component.
- **Lead magnet** — per `style-guides/lead-magnets.md`, if the campaign's funnel calls for a gated asset (or if the business's actual lead magnet is something else, like a free consultation — don't force a downloadable into a funnel that doesn't need one).

### 5. Content calendar
Week-by-week table:

| Week | Content Piece | Format | Channel | Source Skill | Priority | Status |
|---|---|---|---|---|---|---|

"Source Skill" names which `_skills/` entry will actually produce that piece (`social-creative-designer`, `carousel-post-designer`, `ad-creative-designer`, `ai-search-blog-writer`, `lead-magnet`, `repurposing-to-*`) — this calendar is a production plan, not just a content idea list.

### 6. Content assets needed
For every asset in the calendar: type, brief description, priority (must-have vs. nice-to-have), which skill produces it, and whether it also needs `graphic-production-studio` for an actual designed/exported graphic.

### 7. Success metrics
Metrics should match the business's actual situation:
- If the business has campaign history, use real prior benchmarks if available in `memory.md` or elsewhere in the project.
- If this is a new business profile or a new channel for them, **label targets as starting estimates, not validated benchmarks** — don't present a number as proven performance when no campaign has run yet. This matters most for pre-revenue businesses (see `products.md` honesty flags).
- Cover whatever's relevant to the channels actually in use: cost per lead, lead volume, booking/consultation rate (paid); reach, engagement rate, saves, follower growth (organic); open/click rate (email).

### 8. Budget allocation
Only if a real budget was provided — break down by channel/campaign objective. If organic-only, state the actual cost is time, not media spend, and estimate the weekly time commitment instead (see `style-guides/social.md` for any documented time budget).

### 9. Risks and mitigations
Risks specific to this business, not generic ones — e.g. ad fatigue only matters if paid is active; lead quality/qualification risk only matters if the funnel has a qualification step; content-consistency risk matters more for a solo operator than a team with dedicated marketing staff.

### 10. Next steps
Immediate action items, content production priorities, approval checkpoints, launch date.

---

## 4. Quality bar

- Every channel included in the plan is one your business actually has active or is explicitly choosing to activate — nothing defaulted in from a generic campaign template.
- Success metrics are labeled as estimates when no real benchmark exists, never presented as proven numbers.
- The content calendar names a real source skill for every piece — this is a production plan, not a wish list.
- Proof points and messaging respect any honesty flags in `products.md`.
- If `Business/[slug]/context/` was incomplete, that's noted rather than papered over with invented specifics.

## 5. Response behavior

**If the business isn't clear:** ask before planning anything — see Section 1, step 0.

**If given only a goal:** make reasonable assumptions about timeline and channel mix based on `Business/[slug]/context/`, and produce a complete brief rather than asking first — state the assumptions at the top.

**After the brief is saved (see Section 6), confirm both saves happened** — state the file path of the brief saved in `Business/[slug]/examples/` and confirm the proposed calendar rows were appended to `Business/[slug]/social/content-calendar.md`.

**Then ask:** "Want me to start producing the content pieces from the calendar, write the ad copy for a specific campaign objective, draft the email sequence for this campaign's leads, or build out the first two weeks of social captions?" — and route each to the matching content skill rather than writing it inline here.

## 6. Save Your Output

Once the campaign brief is finished, save it automatically — don't ask "should I save this?" first.

1. **Save the full brief** to `Business/[slug]/examples/` as `YYYY-MM-DD_campaign-brief_[campaign-name-slug].md` (today's date, and a slug of the campaign name from Section 3.1).
2. **Append the proposed calendar to the running content calendar.** Dropbox has no in-place append, so: fetch the current contents of `Business/[slug]/social/content-calendar.md`, add the campaign's week-by-week content calendar (Section 3.5) as new rows at the bottom of the existing table, then delete and recreate the file at the same path with the combined content. For these new rows: `Status` = "Planned", `File` = the path of the campaign brief saved in step 1, so each calendar row traces back to the brief that proposed it.


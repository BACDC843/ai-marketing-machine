---
name: ad-creative-brief
description: >
  Produces a structured creative brief — objective, audience, core message, offer, format, and platform — before paid ad creative gets written. Reads brand voice, audience, and products from your Business/[slug]/context/ folder at runtime rather than hardcoding any brand. Use whenever the user asks for an ad brief, wants to plan a paid campaign before writing copy, asks "what should our ad angle be," or is about to run Meta/Facebook/Instagram ads and needs the strategy nailed down first. Feeds directly into ad-creative-designer, which writes the actual ad copy from this brief — use ad-creative-designer directly instead if a clear angle already exists and the user just wants copy written.
---

# Ad Creative Brief

A brief exists to stop money from being spent on the wrong idea. Organic content that misses can be reworked for free; ad spend that misses burns real dollars in hours. This skill's only job is to nail the angle, audience, and offer *before* anyone writes a headline.

Do not write ad copy in this skill — that's `ad-creative-designer`'s job. This skill produces the brief that makes that copy good on the first draft instead of the fifth.

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

1. Read `memory.md` at the project root for active projects and open threads.
2. Read `Business/[slug]/context/brand-voice.md` — positioning, what the brand is and isn't, messaging framework.
3. Read `Business/[slug]/context/audience.md` — who's actually being targeted, their pain points, decision triggers.
4. Read `Business/[slug]/context/products.md` — the real offer, budget tiers, and what "the next step" actually is.
5. Read `Business/[slug]/context/style-guides/ads.md` if it exists — any campaign-type conventions, budget-split guidance, or (critically) whether paid is even an active channel for your business right now.
6. Check `Business/[slug]/examples/` for existing files — especially prior `ad-brief` or `ad-creative` files — first. If any exist, treat them as calibration examples of already-approved work for your business before writing a new brief. This folder may be empty for a business with no history yet; don't block on it.

**If any of these are unfilled placeholders,** say so plainly, then build the brief on whatever real information is available (the request itself, anything mentioned in conversation) rather than inventing brand positioning wholesale.

---

## 2. Brief components

Every brief answers these, in order:

1. **Objective** — what this ad campaign is actually for. Pick one primary objective per brief; a campaign trying to do awareness, lead-gen, and retargeting at once with one ad usually does none of them well:
   - **Lead generation** (cold audience → form fill, DM, or consultation booking)
   - **Retargeting** (warm audience who's already engaged → trust-building, objection handling, push to convert)
   - **Awareness** (cold audience → brand recognition, no hard ask)
2. **Audience segment** — which specific slice of `Business/[slug]/context/audience.md` this ad targets. Not "everyone in the audience file," but pick the segment whose pain point this specific ad speaks to.
3. **Core message / angle** — the one idea the ad is built around, stated in a sentence. If you can't state it in one sentence, the ad doesn't have an angle yet, it has a topic.
4. **The offer** — what happens when someone clicks or responds, pulled from `Business/[slug]/context/products.md`. Never invent an offer that isn't real.
5. **Format recommendation** — image, video, or carousel, based on the objective and what the creative actually needs to show (see `ad-creative-designer` for format-specific specs).
6. **Platform** — Meta (Facebook/Instagram) by default unless `Business/[slug]/context/` or the request specifies otherwise.
7. **Success metric** — what "this worked" looks like for this specific objective (cost per lead, click-through rate, cost per consultation booked, etc. — directionally, not a guaranteed number).

## 3. Campaign-type framework

A useful default split when planning a full paid program rather than a single ad (adjust based on `Business/[slug]/context/products.md` and actual budget):

- **~60% Lead generation** — cold audiences, the specific offer from `Business/[slug]/context/products.md`, a clear single CTA.
- **~30% Retargeting** — warm audiences who've engaged but not converted; lean on trust signals, process transparency, testimonials/proof.
- **~10% Awareness** — cold audiences, brand-building, no hard ask; the long game that makes the other two campaigns cheaper over time.

Don't default to this split silently — state it as the recommendation and let the user adjust.

---

## 4. Output format

```markdown
## Ad Brief — [working title]

**Business:** [business slug]
**Objective:** [lead gen / retargeting / awareness]
**Audience segment:** [specific slice, from Business/[slug]/context/audience.md]
**Core message:** [one sentence]
**Offer:** [from Business/[slug]/context/products.md]
**Format:** [image / video / carousel] — [why]
**Platform:** [Meta / other]
**Success metric:** [directional target]

**Angle rationale:** [2-3 sentences — why this audience, this message, right now]
**What to avoid:** [anything from Business/[slug]/context/brand-voice.md that this angle needs to steer clear of]
```

---

## Save Your Output

Once the brief is finished, save it automatically — don't ask "should I save this?" first — as a new file in `Business/[slug]/examples/`, named:

`YYYY-MM-DD_ad-brief_[short-descriptive-slug].md`

Use today's real date when known (e.g. `2026-07-09_ad-brief_fall-lead-gen-push.md`); if it isn't known at run time, fill it in then. This keeps the finished brief available as a calibration example for future `ad-creative-brief` and `ad-creative-designer` runs — see Section 1, step 6.

---

## 5. Response behavior

**If the business isn't clear:** ask before writing a brief — see Section 1, step 0.

**If `Business/[slug]/context/style-guides/ads.md` says paid isn't currently an active channel for your business:** flag that plainly before proceeding — don't silently assume a paid budget exists just because a brief was requested.

**If given only a topic or goal:** make reasonable assumptions about objective, audience segment, and format, and produce a complete brief rather than asking first — state the assumptions at the top.

**If the user wants multiple angles to choose from:** produce 3 distinct briefs (different core message each, not just different wording of the same angle) and let the user pick before handing off to `ad-creative-designer`.

**After the brief:** note that the brief was saved to `Business/[slug]/examples/[filename]`, that the next step is `ad-creative-designer` to turn this into actual ad copy, and offer to do it now if the user wants to continue immediately.

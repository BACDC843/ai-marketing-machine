---
name: ad-creative-designer
description: >
  Produces paid ad creative — primary text, headline, description, CTA, and visual direction — for Meta (Facebook/Instagram) ads, built to current platform specs and character limits. Reads brand voice, audience, and products from your Business/[slug]/context/ folder at runtime rather than hardcoding any brand. Use whenever the user asks to write ad copy, build a Meta/Facebook/Instagram ad, needs creative for a paid campaign, or has an ad brief ready and wants it turned into actual copy. If there's no clear angle or brief yet, use ad-creative-brief first — this skill writes from a brief, it doesn't set campaign strategy.
---

# Ad Creative Designer

You are writing ad copy that has to work in the first half-second of a feed scroll, against a hard character limit, for money that's actually being spent. This is not organic content — see `social-creative-designer` and `carousel-post-designer` for that — and it's not the strategy layer — see `ad-creative-brief` for that. This skill turns a clear angle into finished, spec-correct ad creative.

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

## 1. Read the business context — and check for a brief

The active business is already resolved. Before doing anything else:

0. **Confirm the business profile.** The active business was resolved once at the top of this skill — don't re-resolve or re-ask here. If no profile exists yet, stop and run `business-setup` rather than writing against an empty context folder.

1. Read `memory.md` at the project root for active projects and open threads.
2. Read `Business/[slug]/context/brand-voice.md` — tone, approved language, messaging framework (most brands' messaging framework is built around AIDA or similar — check what's actually documented rather than assuming).
3. Read `Business/[slug]/context/audience.md` — pain points, decision triggers, the language they use.
4. Read `Business/[slug]/context/products.md` — the real offer; ad copy that promises something not in `Business/[slug]/context/products.md` is a liability, not just weak copy.
5. Read `Business/[slug]/context/style-guides/ads.md` if it exists — check specifically whether paid is even an active channel for your business right now; if not, flag that before proceeding rather than silently assuming a budget exists.
6. **Check for an existing brief** (a recent `ad-creative-brief` output in conversation, or ask if one exists). If there's a clear angle already, use it. If not, don't hard-block — state the assumption you're making about objective/audience/angle and proceed, but flag that running `ad-creative-brief` first would sharpen it.
7. Check `Business/[slug]/examples/` for existing files — especially prior `ad-creative` or `ad-brief` files — first. If any exist, treat them as calibration examples of already-approved work for your business before writing new copy. This folder may be empty for a business with no history yet; don't block on it.

---

## 2. Meta ad specs (current — recheck periodically, these change)

| Element | Spec |
|---|---|
| Feed image | 1080x1080px (1:1) or 1080x1350px (4:5) |
| Stories / Reels | 1080x1920px (9:16) |
| Carousel card | 1080x1080px |
| Primary text | Recommended ~125 characters before truncation risk — write the hook in the first line, it's what shows before "See more" |
| Headline | ~40 characters |
| Description | ~25-30 characters (short supporting line, not a second headline) |
| File size | Images up to 30MB; video up to 4GB |
| Safe zones (Stories/Reels) | Keep key text/logo out of the top ~14% and bottom ~35% of frame — that space is covered by platform UI |
| Links in copy | Don't put URLs in the caption text — they're not clickable there; the actual link lives in the ad's link field |

Ad quality (resolution, relevance, format-fit) affects auction performance directly — a low-res or oddly-cropped asset doesn't just look worse, it costs more per result. Don't downscale creative to save time.

---

## 3. Copy framework — AIDA

Unless `Business/[slug]/context/brand-voice.md` documents a different messaging framework, use AIDA:

- **Attention** (primary text, first line) — the hook. Specific number, bold claim, or a problem the audience recognizes immediately. This is the only line guaranteed to be read before someone decides to expand or scroll past.
- **Interest** — 1-2 sentences that earn the next beat: educate, empathize, or reveal something the audience didn't know.
- **Desire** — paint the outcome specifically, using real detail from `Business/[slug]/context/products.md` — not generic benefit language.
- **Action** — one CTA, matched to the objective from the brief (lead gen wants a form/DM/booking; retargeting wants a lower-friction trust action; awareness may want no hard ask at all).

## 4. Output format

```markdown
## Ad — [working title]

**Business:** [business slug]
**Objective:** [from brief]
**Format:** [image / video / carousel]

**Primary text:**
[full copy, ~125 characters guidance — hook in the first line]

**Headline:** [~40 characters]
**Description:** [~25-30 characters]
**CTA button:** [platform CTA button label, e.g. Learn More / Book Now / Send Message]

**Visual direction:** [what the image/video should show — reference Business/[slug]/context/brand-board.md if it exists]
**Dimensions:** [per Section 2, matched to format and placement]
```

## 5. Output modes

### Mode A — Single ad
Default. One complete ad per Section 4's format.

### Mode B — Variant set
When testing is the goal, produce 2-3 variants that change the **angle**, not just the wording — a different hook, a different pain point, a different proof point. Three versions of the same idea reworded isn't a real test.

---

## 6. Quality bar

- The hook in primary text would stop the specific audience segment from the brief, not just "an audience."
- Copy fits the character guidance in Section 2 — check it, don't eyeball it.
- The offer matches `Business/[slug]/context/products.md` exactly — no invented claims, no promises the brand can't keep.
- Tone matches `Business/[slug]/context/brand-voice.md`.
- CTA matches the objective (don't put a hard lead-gen CTA on an awareness ad).
- Visual direction is specific enough to brief a designer or image generator without more back-and-forth.
- If `Business/[slug]/context/` was incomplete, that's noted rather than papered over.
- If paid isn't an active channel for your business per `Business/[slug]/context/style-guides/ads.md`, that's flagged rather than silently ignored.

---

## Save Your Output

Once the ad creative is finished — and approved by the user if a revision loop happened — save it automatically, without asking "should I save this?" first, as a new file in `Business/[slug]/examples/`, named:

`YYYY-MM-DD_ad-creative_[short-descriptive-slug].md`

Use today's real date when known (e.g. `2026-07-09_ad-creative_fall-lead-gen-hook.md`); if it isn't known at run time, fill it in then. This keeps the finished copy available as a calibration example for future `ad-creative-brief` and `ad-creative-designer` runs — see Section 1, step 7.

---

## 7. Response behavior

**If the business isn't clear:** ask before writing anything — see Section 1, step 0.

**If no brief exists:** state the angle/objective/audience assumption plainly at the top of the output, and suggest running `ad-creative-brief` for anything beyond a single quick ad.

**If given a brief:** follow it — don't second-guess the objective or audience it specifies.

**If asked to revise:** change only what was flagged, and keep the character-limit discipline on the revision too.

**After the final approved version:** save it per the "Save Your Output" section above, and confirm to the user that it was saved to `Business/[slug]/examples/[filename]`.

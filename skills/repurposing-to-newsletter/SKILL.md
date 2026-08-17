---
name: repurposing-to-newsletter
description: >
  Repurpose one piece of existing content — a blog post, social post, case study, or transcript — into a single email newsletter issue or section. Use when the user wants ONE piece of source content adapted into ONE newsletter send, not a multi-email drip sequence (use an email-sequence skill for that). If there is no source content yet, this isn't the right skill — write the original piece first, then repurpose it. Always reads brand voice, audience, and product/offer context from your Business/[slug]/context/ folder before adapting.
---

# Repurposing to Newsletter

Turn one existing piece of content into one newsletter issue (or one section within a larger issue). This is a single-piece adaptation, not sequence-building — it does not plan multi-email funnels or drip logic.

**Scope boundary:** if the user asks for a 3-5 email nurture sequence, a welcome series, or anything with multiple emails building toward a single goal over time, that's a different job — point them to an email-sequence skill if one is installed, instead of building it here.

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

Read (in this order, skip what doesn't exist yet):

1. `Business/[slug]/context/brand-voice.md` — tone, vocabulary, sentence rules
2. `Business/[slug]/context/audience.md` — who's on this list and why they subscribed
3. `Business/[slug]/context/products.md` — the offer/CTA this issue should route toward
4. `Business/[slug]/context/style-guides/social.md` — for any cross-promotion of social content within the newsletter
5. `Business/[slug]/context/style-guides/email-newsletter.md` — any subject line, cadence, or tooling conventions already decided for your business
6. `Business/[slug]/examples/` — check for existing files first; if any exist, treat them as calibration examples of already-approved voice/structure for your business. (May be empty for a business with no history yet — don't block on it.)

If `Business/[slug]/context/` is empty or the business isn't specified, ask before producing anything.

## 2. Get the Source Material

Ask for (or accept if already provided):

- The source content — blog post, social post(s), case study, transcript, or a topic summary
- Whether this is a **standalone issue** (the whole newsletter is about this one piece) or **one section** within a multi-section issue (e.g., a "featured project" block inside a broader company update)
- The sending context if known: list size/segment, typical open behavior, any upcoming send this needs to hit

## 3. Newsletter Structure Baseline

Use this structure (adapted from the `marketing:content-creation` plugin's Email Newsletter Structure, made repurposing-specific — or from `Business/[slug]/context/style-guides/email-newsletter.md` if that client has its own documented format):

- **Subject line**: 2-3 options, under 50 characters, pulls the single most compelling element of the source content (a number, outcome, or curiosity gap) rather than a generic "Newsletter #12" label.
- **Preview text**: 40-80 characters, complements the subject without repeating it — often the second-best hook from the source.
- **Header/hero**: One line framing why this issue matters to the reader right now, plus a hero image direction if the source had strong visuals (before/after, project photo, etc.).
- **Body**: Adapted from the source, restructured for scannable email reading — short paragraphs, one core message, subheads if the source had multiple sections. This is where the actual repurposing work happens (see Section 4).
- **Primary CTA**: One clear action, tied to `Business/[slug]/context/products.md`.
- **Footer**: Standard unsubscribe/contact block — note it's needed but don't attempt to write platform-specific legal/compliance footer text; flag that as the user's/ESP's responsibility.

## 4. Adapting the Source Into Email Form

1. **Cut for skimmability first.** Email readers scan; a blog post's full argument or a carousel's full slide sequence won't survive intact. Identify the 1-3 things this issue needs the reader to take away, and build the body around those, dropping supporting detail that doesn't serve them.
2. **Translate visual-dependent content.** If the source leaned on a carousel or Reel (slide-by-slide reveal, on-screen text), describe the equivalent in prose or convert the slide sequence into a short numbered/bulleted recap — don't just say "see attached" for content that needs to stand on its own in an inbox.
3. **Re-anchor the CTA.** Social CTAs ("DM 'BUILD'," "swipe up") don't work in email. Convert to an email-native action: a link, a reply prompt, a booking link, a download.
4. **Preserve one distinct voice.** If repurposing from a personal-voice LinkedIn post, decide whether the newsletter keeps that first-person voice (common for founder-led newsletters) or reverts to brand voice — state which and stay consistent through the issue.

## 5. Output

Present:

1. **Issue type** — standalone issue or section-within-issue (confirm this matches what the user asked for).
2. **Subject line options** (2-3) and preview text.
3. **Full body copy**, structured per Section 3.
4. **CTA**, explicitly stated as email-native (not a social CTA).
5. **What changed from the source** — brief note on what was cut or restructured for email format.

## 6. Quality Bar

- Reads like an email, not a pasted-in blog post or caption — line length, paragraph breaks, and pacing fit inbox reading.
- One clear takeaway and one clear CTA, even if the source had several.
- Subject line earns the open on its own merit, not just restating the source's headline.
- Does not drift into sequence-building — this produces one issue/section, not a multi-touch plan.

## 7. Response Behavior

If the business isn't clear, ask before doing anything — see Section 1, step 0. If no source content is provided, ask for it. If it's unclear whether this is a standalone issue or one section of a larger send, ask. If the user's request is actually for a multi-email sequence, redirect to `email-sequence` (or the business-specific equivalent) rather than building a sequence here.

After delivering, ask: "Want this adapted for Instagram or LinkedIn too, or should I draft a second section for the same issue?"

**Once the issue is delivered:** save it automatically to `Business/[slug]/examples/` per Section 8 (no need to ask "should I save this?" first), and confirm the save in your response with the file path (e.g. "Saved to `Business/[slug]/examples/2026-07-09_newsletter_[slug].md`").

## 8. Save Your Output

Once the newsletter issue (or section) is finished and delivered, save it as a new file in `Business/[slug]/examples/` named `YYYY-MM-DD_newsletter_[short-descriptive-slug].md` — use today's real date (e.g. `2026-07-09_newsletter_summer-project-recap.md`) if known at run time, otherwise fill in the actual send/creation date when saving. This is a universal convention across the content skills: `Business/[slug]/examples/` is the finished-copy archive every skill reads from first (see Section 1, step 6) and writes to on completion, so future runs — and other skills — have real, approved examples to calibrate against. Save automatically every time; don't ask permission first.

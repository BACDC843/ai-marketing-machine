---
name: repurposing-to-linkedin
description: >
  Repurpose existing content — a blog post, video/Reel transcript, case study, or another platform's post — into LinkedIn-native formats (personal-voice post or multi-slide document post). Use when source content already exists and needs a LinkedIn-specific version, especially when adapting consumer-facing content for B2B audiences. If there is no source content yet, use social-creative-designer or carousel-post-designer to originate content from scratch instead. Always reads brand voice, audience, and platform style from your Business/[slug]/context/ folder before adapting.
---

# Repurposing to LinkedIn

Turn existing content into LinkedIn-native posts. Like `repurposing-to-instagram`, this skill extracts and translates rather than originates — but LinkedIn requires a heavier rewrite than Instagram does, because the platform rewards a different register: personal, credible, depth-over-virality, professional-but-human.

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
2. `Business/[slug]/context/audience.md` — who's reading, and whether this audience includes B2B/professional segments
3. `Business/[slug]/context/products.md` — offers/CTAs to route toward
4. `Business/[slug]/context/style-guides/social.md` — posting cadence, hashtag policy (LinkedIn uses hashtags far more sparingly than Instagram)
5. `Business/[slug]/context/brand-board.md` — colors/fonts if producing a document-post design alongside copy

Also check `Business/[slug]/examples/` for existing files first — if any exist, treat them as calibration examples of already-approved voice/structure for your business's LinkedIn content. This folder may be empty for a business with no history yet; don't block on it if so.

If `Business/[slug]/context/` is empty or the business isn't specified, ask before producing anything.

## 2. Get the Source Material

Ask for (or accept if already provided):

- The source content — blog post, transcript, case study, Instagram/Facebook post, email
- Who's posting it: the brand/company itself, or a named individual (founder, agent, principal)? LinkedIn's algorithm and audience both favor personal profiles over company pages — if there's a real person to post as, prefer that.
- Which format: single post or document post (carousel-style PDF), or "not sure, recommend one"

## 3. Why LinkedIn Is Different From Instagram

LinkedIn's "Authenticity Update" (2025-2026 era) shifted the algorithm to favor personal, experience-based posts and document posts over polished/promotional content and hashtag-stuffed posts. Concretely, for repurposing decisions:

- **Reframe from brand voice to a person's voice where possible.** A post that works as "[Business] transformed this 1920s home" on Instagram often performs better on LinkedIn reframed as "I walked through a 1920s home in Harleston Village last month that most contractors would have gutted. Here's why we didn't." — first-person, specific, a little vulnerable about the reasoning, not just the result.
- **Document posts (multi-slide PDF-style carousels) get strong engagement** — 6.6%+ engagement rates have been reported for this format vs. standard image posts. A blog post or Instagram carousel with a clear step/list structure is a strong candidate for this format.
- **Depth beats virality.** LinkedIn audiences reward posts that teach something or reveal reasoning, not just posts that look good. When compressing source material, keep the "why," not just the "what."
- **Hashtags and polls are used sparingly**, if at all, under the current algorithm — don't port over an Instagram-style hashtag block.

## 4. B2B reframing

Consumer-facing content sometimes needs to speak to a different audience on LinkedIn — builders, architects, remodelers, and small business owners considering the business as a vendor or partner, not a consumer considering a purchase. When repurposing for this audience:

- Shift the "so what" from "here's a beautiful result" to "here's how this was executed" or "here's what this signals about working with us." Professional audiences care about process, reliability, and craft as *evidence of competence*, not just aesthetics.
- Swap consumer CTAs ("DM 'BUILD'") for professional ones ("Let's talk about your next project," "Open to a conversation about partnering on X").
- Check `Business/[slug]/context/audience.md` for whether a B2B segment is defined; if not, ask the user whether this post is aimed at homeowners/consumers or at industry peers/partners before rewriting the register.

## 5. Extraction Patterns by Format

### Personal-Voice Post

1. Identify the single strongest insight, lesson, or moment in the source — LinkedIn posts work best around one idea explored with some depth, not a compressed list.
2. Open with a concrete, specific first line — a moment, a number, a decision point. Avoid generic openers ("I've been thinking about...").
3. Develop the idea in 3-6 short paragraphs (1-2 sentences each, LinkedIn's line-break-heavy reading pattern). Include the reasoning, not just the outcome.
4. Close with a direct takeaway or question that invites comment — LinkedIn's algorithm still weights comments heavily.
5. One CTA, softer/more conversational than Instagram's.

### Document Post (Multi-Slide)

1. Identify the step-by-step, listicle, or before/after structure in the source.
2. Hand off to `carousel-post-designer` for the slide-by-slide build, noting that LinkedIn document posts run longer than Instagram carousels (7-12 slides is common) and use a more text-forward, less design-heavy layout — cover slide with a clear promise, then one idea per slide, close with a CTA slide.
3. Keep the visual design more restrained than an Instagram carousel — LinkedIn audiences respond to document posts that read like a mini-guide, not an ad.

## 6. Output

Present:

1. **Format chosen** (personal post vs. document post) and one-line reasoning.
2. **Posting voice** — flag explicitly whether this is written as the brand or as a named individual, and who.
3. **The repurposed content** in full.
4. **What changed from the source**, including any register shift made for a B2B audience.

## 7. Quality Bar

- The post sounds like it belongs on LinkedIn, not like an Instagram caption with the emojis removed.
- If reframed to a personal voice, it's consistent — doesn't drift back into brand-speak halfway through.
- B2B reframing (if applicable) actually changes the "so what," not just the CTA.
- No hashtag-stuffing or Instagram-style formatting habits carried over.

## 8. Save Your Output

Once the repurposed piece is finished — and approved by the user if a revision loop was used — save it automatically, without asking "should I save this?" first:

1. Save the finished piece as a new file in `Business/[slug]/examples/`, named `YYYY-MM-DD_linkedin-repurpose_[short-descriptive-slug].md` (today's date, and a short slug describing the piece).
2. Append a new row to `Business/[slug]/social/content-calendar.md` with columns `Date | Format | Channel | Summary | Status | File` — Channel is "LinkedIn," Status is "Draft" unless the user has said this piece is already scheduled or published, and File is the path just saved to `Business/[slug]/examples/`.

Do this every time a piece is finished, regardless of format (personal-voice post or document post) — the business's `Business/[slug]/examples/` archive and `Business/[slug]/social/content-calendar.md` should always reflect what's been produced.

## 9. Response Behavior

If the business isn't clear, ask before doing anything — see Section 1, step 0. If no source content is provided, ask for it. If the audience (consumer vs. B2B/industry) isn't clear from `Business/[slug]/context/` or the request, ask which one this post is for before writing — the voice and CTA depend on it. Otherwise, produce the repurposed content directly.

After delivering, confirm both saves happened — state the exact file path saved to `Business/[slug]/examples/` and confirm the row was appended to `Business/[slug]/social/content-calendar.md`. Then ask: "Want this adapted for Instagram or a newsletter too, or should I draft it as a document post instead?"

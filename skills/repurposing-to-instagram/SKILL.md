---
name: repurposing-to-instagram
description: >
  Repurpose existing content — a blog post, video/Reel transcript, podcast excerpt, email, or another platform's post — into Instagram-native formats (single post, carousel, or Reel script). Use when the user has source content already written or filmed and wants an Instagram-specific version of it, not a brand-new post from a bare topic. If there is no source content yet, use social-creative-designer (single/multi-image posts) or carousel-post-designer (carousels) instead to originate content from scratch. Always reads brand voice, audience, and platform style from your Business/[slug]/context/ folder before adapting — never hardcode a brand's voice or visuals.
---

# Repurposing to Instagram

Turn existing content into Instagram-native posts. This skill's job is **extraction and translation**, not origination — the ideas, proof points, and structure already exist in the source; the work is deciding what survives the move to Instagram and what has to change.

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
2. `Business/[slug]/context/audience.md` — who's scrolling, what they care about
3. `Business/[slug]/context/products.md` — offers/CTAs to route toward
4. `Business/[slug]/context/style-guides/social.md` — posting cadence, hashtag policy, emoji policy
5. `Business/[slug]/context/brand-board.md` — colors/fonts if a visual asset is being produced alongside the copy

Also check `Business/[slug]/examples/` for existing files first — if any exist, treat them as calibration examples of already-approved voice/structure for your business's Instagram content. This folder may be empty for a business with no history yet; don't block on it if so.

If `Business/[slug]/context/` is empty, run `business-setup` before producing anything — do not default to any previously-used brand's voice.

## 2. Get the Source Material

Ask for (or accept if already provided in the conversation):

- The source content itself — full blog post text, video/Reel transcript, podcast excerpt, email copy, or a LinkedIn/other-platform post
- What made this piece work, if the user knows (a specific stat, story beat, or reaction it got)
- Which Instagram format they want out of it — single post, carousel, or Reel script — or "not sure, recommend one"

Do not invent source content. If the user says "repurpose my blog post" without pasting or linking it, ask for the text before proceeding.

## 3. Choosing the Right Format

| Source has... | Best Instagram format | Why |
|---|---|---|
| One strong idea, stat, or story | Single post | Doesn't need slides to carry it |
| 3+ distinct ideas, steps, or a listicle structure | Carousel | Each idea becomes its own slide — hand off to `carousel-post-designer` for the slide-by-slide build |
| A demonstrated process, transformation, or talking-head moment | Reel script | Motion/voice carries it better than static images |
| A long-form narrative or case study | Carousel (story arc) or single post (if one moment is strong enough to stand alone) | Depends on whether the value is in the journey or the punchline |

If unsure, recommend one format and explain why in one sentence, rather than producing all three by default — that triples the work for content that may not need it.

## 4. Instagram Mechanics (Condensed)

For the full platform-mechanics writeup (algorithm behavior, saves/shares/completion rate, caption length, hashtag strategy), see `social-creative-designer`'s Platform Mechanics section — this skill doesn't duplicate it. The condensed version relevant to repurposing:

- Instagram rewards content that gets saved, shared, and watched/read to completion — not just liked. When trimming source material down, protect the parts most likely to be saved or shared (the single most useful line, stat, or step), not just the parts that sound good.
- Captions: hook in the first line (visible before "more"), short paragraphs, one CTA.
- Carousels get algorithmic credit for multi-swipe sessions and get resurfaced — a listicle-style blog post is often a better carousel than a single post.

## 5. Extraction Patterns by Format

### Single-Post Extraction

1. Identify the single strongest idea in the source — the one sentence someone would screenshot or send to a friend.
2. Rewrite it as an Instagram hook (first line) using the brand voice's hook patterns.
3. Compress supporting context to 2-4 body lines. Cut anything that only made sense in the original long-form format (e.g., "as I mentioned earlier" or "in section 3").
4. Add one CTA from `Business/[slug]/context/products.md`.
5. Flag what's lost: if the source had nuance or caveats that don't survive compression, say so in one line to the user rather than silently dropping them.

### Carousel Extraction

1. Identify the 4-10 distinct ideas, steps, or sections in the source.
2. Rank them — cut the weakest until what's left is genuinely one-idea-per-slide, not padded to hit a slide count.
3. Hand off to `carousel-post-designer` using its slide structures and copy rules — pass along the ranked idea list as the slide content plan so it doesn't have to re-derive structure from scratch.
4. Note which slides are near-verbatim from the source vs. rewritten for brevity, so the user can spot-check compression accuracy.

### Reel Script Extraction

1. Find the moment in the source with visible action, transformation, or a clear before/after — Reels underperform when built from purely textual/abstract source material.
2. Structure: **Hook** (0-2 sec, on-screen text + voiceover line, must stop the scroll) → **Middle** (process/proof, show don't just tell) → **Close** (payoff + CTA).
3. Write on-screen text separately from voiceover — they should reinforce, not duplicate, each other word-for-word.
4. Suggest a visual/shot list only if the user has footage to work with; otherwise flag that this format requires filming, not just editing existing assets.

## 6. Output

Present:

1. **Format chosen** and one-line reasoning (skip if the user specified the format).
2. **The repurposed content** in full, ready to post.
3. **What changed from the source** — a short note on what was cut, compressed, or reframed, so the user can sanity-check against the original.
4. Hashtag set per `Business/[slug]/context/style-guides/social.md` if the format is a feed post/carousel.

## 7. Quality Bar

- Every idea in the output actually traces back to the source — this skill adapts, it doesn't invent new claims.
- The brand voice from `Business/[slug]/context/` is applied to the *rewrite*, even when the source material was written in a different voice (e.g., repurposing a formal blog post into a punchier Instagram caption).
- Compression is disclosed, not silent.
- No other business's brand voice, colors, or fonts carry over from a previous request — always re-read `Business/[slug]/context/` for the business named in this request.

## 8. Save Your Output

Once the repurposed piece is finished, save it automatically — do not ask "should I save this?" first:

1. Save the finished piece as a new file in `Business/[slug]/examples/`, named `YYYY-MM-DD_instagram-repurpose_[short-descriptive-slug].md` (today's date, and a short slug describing the piece).
2. Append a new row to `Business/[slug]/social/content-calendar.md` with columns `Date | Format | Channel | Summary | Status | File` — Channel is "Instagram," Status is "Draft" unless the user has said this piece is already scheduled or published, and File is the path just saved to `Business/[slug]/examples/`.

Do this every time a piece is finished, regardless of format (single post, carousel, or Reel script) — the business's `Business/[slug]/examples/` archive and `Business/[slug]/social/content-calendar.md` should always reflect what's been produced.

## 9. Response Behavior

If the user hasn't provided source content, ask for it before doing anything else.  Otherwise, produce the repurposed content directly — this skill doesn't need an approval-gate planning stage the way `carousel-post-designer` does for original content, since the source material already constrains the ideas.

After delivering, confirm both saves happened — state the exact file path saved to `Business/[slug]/examples/` and confirm the row was appended to `Business/[slug]/social/content-calendar.md`. Then ask: "Want this adapted for LinkedIn or a newsletter too, or should I package this as a Reel script instead?"

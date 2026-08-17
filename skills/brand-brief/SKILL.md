---
name: brand-brief
description: Captures a business's brand voice, audience, and messaging wedge through a few quick conversational questions, then saves it to brand-brief.md so every other content skill (post-writer, content-coach, post-grader) can write on-brand without re-asking. Triggers when brand-brief.md is missing and a content skill needs it, or when the user explicitly asks to set up or update their brand brief.
---

# Brand Brief

You capture the minimum viable brand context a small business owner needs so every content skill downstream — `post-writer`, `content-coach`, `post-grader` — can write in their voice, for their audience, without asking the same questions every session.

This is scaffolding, not a deliverable. The user rarely needs to see the raw file; they need the content that gets written from it to sound like them.

## Where your brand context lives — resolve this before reading or writing it

Brand context is durable memory; it has to outlive the session. Resolve it **once**, in this order:

1. **Business profile — authoritative.** The current project folder is your workspace root, unless `aimm-config.md` at that root sets `workspace_root` (and, with `storage_mode: dropbox`, is read and written through the Dropbox MCP tools at exactly that path). Read `Business/[slug]/context/brand-voice.md`, `audience.md`, and `products.md`. The slug comes from `aimm-config.md` (`business:`), or the single folder under `Business/` that isn't `_template`; if several exist and the config is silent, ask once.
2. **`brand-brief.md` at the workspace root — fallback only.** Use it when no business profile exists. If you capture or update a brief, write it here. In Dropbox mode there is no in-place edit: fetch the live file, then delete and recreate it at the same path.
3. **Neither reachable.** Say so in one line, work from what you're told this session, and do not claim anything was saved.

If both exist, the profile wins and the brief is treated as older notes — never blend a contradiction silently; say which one you used in one line.

**Before falling back to a lesser path,** check `.aimm/environment.md` for what `doctor` last found. Treat it as a hint, not proof — if it is stale or absent, probe and proceed. The live probe is always authoritative.

Never write brand context only to the session's working directory. That container is discarded, so "saved" would be false and the next session would re-ask every question.

---

## When to Activate

- Auto-invoked by `content-coach` Step 2 when no brand context exists at all (resolved above)
- "Set up my brand brief" / "let's define my brand voice"
- Any content skill needs brand context and none exists yet
- The user says a draft "doesn't sound like me" and there's no brief to check against

## Workflow

### Step 1: Check for an existing brief first

Check the brand context resolved above before asking anything. If a business profile exists, read it and update that rather than writing a competing brief. If a `brand-brief.md` exists, read it and skip to **Updating an Existing Brief** below instead of starting over.

### Step 2: Ask the questions conversationally, one at a time

Don't dump all of these in one message — that's the fastest way to lose a nervous first-time user. Ask, wait for the answer, then ask the next one.

1. What's your business — what do you sell?
2. Who's your customer — describe one real person who buys from you.
3. What's the one action you want a reader to take (buy, sign up, follow, DM)?
4. Tell me one recent story, win, or thing that happened in your business.
5. What's your vibe — fun and casual, professional, raw and honest, witty?
6. What's one opinion you hold about your industry that a lot of people in it would disagree with?

Q6 is the **wedge** — the single highest-leverage input for viral content later (see `content-coach`'s ideation step, which pulls directly from it for the "polarizing opinion" angle). It's also the one people freeze on. If they draw a blank, offer to skip it and come back later — a brief missing the wedge is still usable, just weaker for that one angle.

### Step 3: Save to brand-brief.md

Save the answers to `brand-brief.md` at the workspace root (resolved above), using the template below. If a business profile exists, write the same answers into its `context/` files instead — the profile is authoritative and two brand sources must never disagree. Every future session's content skills read this file — treat it as durable brand memory, not a one-off Q&A transcript.

## brand-brief.md Template

```markdown
# Brand Brief — [Business Name]

**Last updated:** [date]

## Business
[What they sell / do — 1-2 sentences]

## Customer
[The one real person description — who they are, what they need, why they buy]

## Primary CTA
[The one action: buy / sign up / follow / DM / etc.]

## Recent Story
[The win, launch, or thing that happened — reusable as content fodder]

## Voice / Vibe
[fun and casual / professional / raw and honest / witty / etc. — 1-2 descriptive sentences, not just the label]

## Strong Opinion / Wedge
[Their contrarian industry take, if given. Highest-virality input for content-coach's ideation step. Write "Not yet captured" if skipped, so downstream skills know to ask again before leaning on polarizing angles rather than silently treating it as blank-on-purpose.]
```

### Step 4: Confirm and hand back

Show the user the filled brief back in plain language — not the raw markdown dump — and confirm it's accurate before handing control back to whichever skill invoked you (usually `content-coach`'s Step 3, moving into idea brainstorming).

## Updating an Existing Brief

If `brand-brief.md` already exists and the user wants to change something ("my vibe isn't right," "we added a new product," "that story's stale now"), read the current file, ask only about what's changing, and update that section in place. Don't re-run all 6 questions — that wastes their time and risks losing context they already gave you.

## What NOT to Do

- Don't ask all 6 questions in one message. One at a time, conversational — this mirrors `content-coach`'s own rule of never front-loading more than 5 questions before showing something back.
- Don't move on to content generation without at least the first 5 answered. Voice and audience are load-bearing for every downstream skill — a brief missing those isn't a shortcut, it's a broken foundation.
- Don't force the Strong Opinion / Wedge question if the user is clearly stuck or uncomfortable. Offer to skip and revisit — some people need a few posts under their belt before they're willing to be polarizing.
- Don't overwrite an existing `brand-brief.md` wholesale when the user only wanted one field updated.
- Don't show them the raw file by default. The brief is internal scaffolding — summarize it back conversationally instead.

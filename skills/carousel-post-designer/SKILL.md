---
name: carousel-post-designer
description: >
  Designs multi-slide carousel posts — Instagram/Facebook swipe carousels and LinkedIn document posts (PDF carousels) — from a topic or rough idea through slide-by-slide copy and strategic visual direction. Reads brand voice, audience, and visual identity from Business/[slug]/context/ at runtime rather than hardcoding any brand. Use whenever the user asks for a carousel, a swipe post, a multi-slide post, a LinkedIn document post, "turn this into slides," or wants an idea broken into slide-by-slide posts — even without naming a platform. For single-image posts, use social-creative-designer. For paid ads, use ad-creative-designer. For an exported graphic once slide copy is approved, hand off to graphic-production-studio — this skill produces strategy and copy, not pixels.
---

# Carousel Post Designer

You are turning ideas into carousel posts that are genuinely useful, readable, and worth swiping through — not generic slide decks with a logo slapped on. Every carousel needs a clear angle, one idea per slide, mobile-readable copy, and a reason someone would stop, swipe, save, share, comment, or follow.

Do not produce a text dump split arbitrarily across slides. If a slide doesn't earn its place, cut it.

This skill's job stops at strategy, slide-by-slide copy, and visual *direction* — the actual design/export work (design briefs, image-generation JSON, HTML/PNG export) lives in `graphic-production-studio`, which every content skill in this project shares. See Section 7 for the handoff.

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

This skill is intentionally brand-agnostic — it doesn't know who it's designing for until it reads `Business/[slug]/context/`. Before producing a carousel:

1. Read `memory.md` at the project root for active projects and open threads.
2. Read `Business/[slug]/context/brand-voice.md` — tone, personality, approved language, words to avoid.
3. Read `Business/[slug]/context/audience.md` — who this is for, their pain points, objections, and the language they use.
4. Read `Business/[slug]/context/products.md` — what's actually being offered, so slides don't drift into vague claims.
5. Read `Business/[slug]/context/style-guides/social.md` and `Business/[slug]/context/style-guides/visuals.md` — platform conventions and visual rules already decided for your business.
6. Read `Business/[slug]/context/brand-board.md` — colors, typography, logo rules, imagery style, for the visual direction you'll hand to `graphic-production-studio`. If `brand-board.md` is still an unfilled placeholder, say so and note that visual direction will be generic until it's filled in.
7. Check `Business/[slug]/examples/` for existing finished carousels. If any exist, treat them as calibration examples of already-approved voice and structure for your business, and read them before writing new content. This folder may be empty for a business with no history yet — that's fine, don't block on it.

**If any context file is still an unfilled placeholder,** say so plainly in the output, then proceed on reasonable defaults inferred from the brief and general best practice. Don't block the request over missing context.

---

## 2. Why carousels, and what actually works (revisit as platforms change)

This reflects carousel mechanics as of mid-2026 — these shift, so don't treat this as permanent.

- **Instagram**: carousels currently outperform single images and often Reels for saves, shares, and deeper engagement — each swipe counts as an interaction, so completion rate (how many people swipe to the last slide) is a meaningful ranking signal, not just an experience nicety. Carousels also get a "second chance": Instagram reshows them to people who scrolled past without engaging the first time. A reasonable content mix for an account leaning into this is roughly 60% carousels / 30% Reels / 10% static. Educational, tips, checklist, and before/after carousels tend to run 8-12 slides; punchier idea-based carousels run shorter.
- **LinkedIn**: multi-slide **document posts** (uploaded as a PDF, swiped like a carousel) are one of the strongest-performing organic formats on the platform right now — meaningfully outperforming plain text posts. The cover slide (page 1) has to earn the open: bold, large text (roughly 40pt-equivalent), minimal clutter, one clear visual element. 7-12 slides is the effective range. Early engagement in the first hour matters for how far it travels.
- **Facebook**: carousels work well for sequential storytelling — before/after, step-by-step process, "here's what a project looked like start to finish" — and for local/community accounts, pairing a carousel with a comment-inviting caption outperforms a broadcast-style caption.
- **Underlying psychology**: a carousel works because each slide is a small, resolved unit that creates a "micro-reward" for swiping — curiosity opened on one slide, satisfied or built on by the next. A carousel that front-loads everything on slide 1 kills its own reason to swipe.

---

## 3. Default slide structure

Unless the user specifies otherwise, use a **6-slide** structure for Instagram/Facebook and treat LinkedIn document posts as the same shape stretched to 7-12 slides when the topic warrants it.

### Default 6-slide structure
1. **Hook** — a scroll-stopping claim, question, problem, or specific number. This is the only slide guaranteed to be seen before someone decides whether to swipe.
2. **Context / tension** — what most people miss, misunderstand, or get wrong about this topic.
3. **Core insight** — the main point or belief shift.
4. **Example or proof** — a specific detail, process point, or real situation that backs up slide 3. Specificity is what makes a carousel feel earned instead of generic.
5. **Takeaway** — what the audience should notice, ask, or do differently, phrased practically.
6. **Close / CTA** — one strong closing line, action, or invitation. Not a repeat of slide 1.

### Extended structure (7-12 slides, LinkedIn document posts or deep educational content)
Add slides by splitting slide 3 (core insight) into 2-3 sequential insights, or slide 4 (proof) into multiple examples — never by padding with filler transition slides. Every added slide must carry a new idea.

### Zone model (useful for any length)
Think in four zones rather than a fixed slide count: **Cover** (earns the swipe) → **Context** (frames why this matters) → **Body** (the actual teaching — one idea per slide) → **CTA** (one clear close). This is the shape to reach for when a topic doesn't map cleanly onto the 6-slide default.

---

## 4. Approval-first planning mode

When the user says "plan first," "don't build yet," "show me the direction," or is choosing between several ideas, do not write full slide copy. Instead, give:
- Slide role (per Section 3)
- Working headline for that slide
- One-line description of what it covers
- Visual direction in one line

Then stop and wait for approval before writing full copy.

---

## 5. Copy rules

- Each slide carries exactly one idea. If a slide needs "and" to describe its content, split it.
- Copy must be readable in under two seconds — this is a mobile, thumb-scrolling format, not a document to be studied.
- No slide should be a wall of text. If `Business/[slug]/context/style-guides/social.md` doesn't specify a line-count ceiling, default to roughly 15-25 words of body copy per slide, less on the hook.
- Use specific language pulled from `Business/[slug]/context/products.md` and `Business/[slug]/context/audience.md` over generic claims. "Custom-fit for a 1920s timber-frame house" beats "quality craftsmanship."
- The caption (posted alongside the carousel) should complement the slides, not repeat them — use it to add a layer the slides didn't cover, or to prompt the specific engagement action.

### Hook slide (slide 1) formulas
- Specific number or stat the audience will recognize as true
- A common mistake, named directly
- A contrarian reframe of conventional wisdom in this space
- A recognizable scene or moment from the audience's own experience
- A direct question in the audience's own words (check `Business/[slug]/context/audience.md`)

---

## 6. CTA system

Pull the actual offer/next-step from `Business/[slug]/context/products.md` — don't invent a generic CTA. Vary CTA type across a batch:
- Save/share prompts ("save this for your next [X]")
- Comment/DM keyword prompts (only if the account actually monitors and responds to these)
- Link-in-bio or landing-page prompts
- No CTA at all — some carousels exist purely to build trust or demonstrate expertise, and a forced CTA on those reads as try-hard

Roughly: 50% save/share, 25% comment/DM, 15% link, 10% no CTA — adjust per what `Business/[slug]/context/products.md` and the campaign goal actually call for.

---

## 7. Output modes

### Mode A — Quick carousel package
Default for a single carousel request. Output:
1. Title / working name
2. Strategic angle (why this, why now, for this audience)
3. Slide-by-slide copy (headline + body + visual direction per slide, per the format in Section 8)
4. Caption
5. CTA options
6. Hashtags (Instagram/LinkedIn only, per social-creative-designer's platform guidance — skip for Facebook)

### Mode B — Approval-first batch
Use when the user asks for multiple concepts. Step 1: give 5 titles, one-sentence concept, target audience, and why each would earn a swipe — then stop. Step 2, after approval: expand only the approved concepts into full slide-by-slide packages.

### Mode C — Full matrix immediately
Use only if the user explicitly asks to skip approval. Same output as Mode B step 2, for all concepts, without pausing.

### Design brief, JSON prompts, or HTML/PNG export — hand off to graphic-production-studio
Once slide copy is written and approved (Mode A, B, or C output), if the user wants a design brief for a human designer, image-generation JSON prompts, or an actual HTML preview / exported PNGs, invoke `graphic-production-studio` and pass it:
- Asset type: `carousel_slide`
- The approved slide-by-slide copy from this skill
- The business slug (so it reads the same `Business/[slug]/context/brand-board.md`)

Don't attempt to reproduce design-system tokens, JSON templates, or the Playwright export pipeline here — that engine is shared across every content skill in this project and lives in one place so its sandbox caveats (Chromium availability, image download/expiry handling) only need to be maintained once.

---

## 8. Slide copy format

```markdown
### Slide 1 — Hook
**Headline:** [short headline]
**Body:** [1-3 short lines]
**CTA:** [only if this slide needs one]
**Visual:** [what the image should show, referencing Business/[slug]/context/brand-board.md for style — this is direction for graphic-production-studio, not a finished design]
```

---

## 9. Quality bar

Before delivering, check the output against this:

- Slide 1 has a real hook, not a bland title.
- Every slide adds a new idea — nothing is padding.
- Copy is short enough to read in under two seconds per slide.
- The tone matches `Business/[slug]/context/brand-voice.md`.
- Visual direction is specific (mood, layout, image type) and references real values from `Business/[slug]/context/brand-board.md`, not invented ones — even though the actual design happens in `graphic-production-studio`.
- CTA fits the topic, audience, and platform.
- Caption complements the slides rather than repeating them.
- If `Business/[slug]/context/` was incomplete, that's noted rather than papered over.
- No generic AI phrasing, no filler slides, no corporate-brochure energy.

---

## 10. Save Your Output

A carousel is finished once its full slide-by-slide package — title, strategic angle, all slide copy, caption, and CTA — has been delivered per Section 7, and after any approval step in this skill's flow (Section 4's plan-first pause, or Mode B's concept approval) has actually been cleared, not just the plan or concept list. Once a carousel reaches that point, save it automatically as the last step of producing it — don't ask the user whether to save first.

1. Check `Business/[slug]/examples/` for existing files (you should already have done this in Section 1, step 7) so the new file's naming and structure stays consistent with what's already there.
2. Save the finished package as a new file in `Business/[slug]/examples/`, named `YYYY-MM-DD_carousel_[short-descriptive-slug].md`. Use today's real date if it's known from context; otherwise, note plainly in the filename or file content that the date placeholder needs to be filled in at run time. The file should contain the full finished package — title, strategic angle, all slide copy (headline, body, CTA, visual direction per slide), caption, and CTA options.
3. Append one row to `Business/[slug]/social/content-calendar.md` with columns `Date | Format | Channel | Summary | Status | File`. Status is "Draft" unless the user has said the carousel is scheduled or published. File is the path just saved in step 2. Dropbox has no in-place append, so: fetch the current `content-calendar.md` content, add the new row at the bottom of the table, then delete and recreate the file with the full updated content.
4. This save step is independent of the handoff to `graphic-production-studio` in Section 7 — the copy gets saved here regardless of whether a design brief, JSON prompts, or an export is also requested for the same carousel.
5. If the user requests edits after the initial save (Section 11 below), update the saved file in `Business/[slug]/examples/` (delete + recreate with the revised copy) rather than creating a second file, and don't add a duplicate content-calendar row for the same carousel.

---

## 11. Response behavior

**If the business isn't clear:** ask before designing anything — see Section 1, step 0.

**If given only a topic:** make reasonable assumptions (platform, slide count, audience, CTA) and produce a complete carousel package rather than asking first — state the assumptions at the top of the output.

**If asked for a plan:** use Section 4 (approval-first) and stop before writing full copy.

**If asked for "the same treatment" as a prior carousel:** match the prior approved structure, voice, and visual logic while adapting the angle to the new topic.

**If asked for edits:** update only the requested slides. Don't rebuild the whole carousel unless the direction fundamentally changes.

**If asked for the actual designed graphic, JSON prompts, or an export:** hand off to `graphic-production-studio` per Section 7 rather than attempting it here.

**Once the carousel is finished and saved (Section 10):** confirm in your closing response that both saves happened, and give the exact paths — the finished package saved to `Business/[slug]/examples/[filename]` and the row appended to `Business/[slug]/social/content-calendar.md`.

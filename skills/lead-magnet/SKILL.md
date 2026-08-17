---
name: lead-magnet
description: >
  Creates gated downloadable lead-generation assets — checklists, guides, templates, and similar — that trade real value for an email address or contact info. Reads brand voice, audience, and products from your Business/[slug]/context/ folder at runtime rather than hardcoding any brand. Use whenever the user asks for a lead magnet, a downloadable guide, a checklist, a freebie, an opt-in offer, or content designed to capture leads in exchange for something valuable — even if they just describe wanting "something to get emails" or "a give-away."
---

# Lead Magnet

A lead magnet that doesn't get used is worse than no lead magnet — it trains people to distrust the next opt-in offer too. The bar is: would someone actually open this, get real value from it in under ten minutes, and think better of the brand afterward? "Join our newsletter" is not a lead magnet. This skill produces the actual asset content, not just an idea.

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
2. Read `Business/[slug]/context/brand-voice.md` — tone, vocabulary.
3. Read `Business/[slug]/context/audience.md` — pain points, where they are in their decision process, the language they use.
4. Read `Business/[slug]/context/products.md` — the paid offer this lead magnet should lead toward. A good lead magnet is a small, free preview of the value in the real offer — not a random tangent.
5. Read `Business/[slug]/context/style-guides/lead-magnets.md` if it exists — some businesses' actual primary lead magnet is something other than a downloadable (e.g. a free consultation) that a downloadable asset should support rather than compete with.
6. Check `Business/[slug]/examples/` for existing files first — if any exist, treat them as calibration examples of already-approved voice/structure for your business. (May be empty for a business with no history yet — don't block on it.)

**If any of these are unfilled placeholders,** say so, then proceed on the brief and general best practice rather than blocking.

---

## 2. What makes a lead magnet actually convert

- **Solves one specific problem** — not "everything you need to know about X," but the one sharp question the audience is actually asking right before they'd reach out.
- **Delivers a quick win** — usable in under ten minutes, not a 40-page ebook nobody finishes.
- **Closely tied to the paid offer** — someone who uses this magnet and gets value should be a *better* lead for the real product, not just any warm body. This is a feature, not a limitation: a magnet with no connection to `Business/[slug]/context/products.md` collects the wrong leads.
- **Minimal friction to get it** — the asset should be genuinely quick to consume; don't gate it behind more questions than necessary to follow up.
- **Specific over generic, local over broad where relevant** — for a locally-rooted brand, a hyperlocal or personalized angle (a checklist specific to the audience's actual city, project type, or budget tier) converts better than a generic industry version of the same asset.

## 3. Format selection

Pick the format based on what the audience actually needs at their stage, cross-referenced with `Business/[slug]/context/products.md`:

| Format | Best for | Typical length |
|---|---|---|
| **Checklist** | A process with real steps the audience is about to go through | 1 page, 8-15 items |
| **One-page guide / cheat sheet** | A concept that needs explaining, not just listing | 1 page, scannable sections |
| **Template** | A document the audience will actually fill in or reuse | The template itself + 3-5 lines of instructions |
| **Resource roundup** | Curated recommendations in a space the audience is researching | 1-2 pages, organized by category |
| **Budget/planning worksheet** | High-consideration purchases where planning is the barrier | 1 page, structured fields |
| **Short assessment/quiz** | When personalized results would genuinely help the audience decide | 5-8 questions + result guidance |

Default to checklist or one-page guide unless the topic clearly calls for something else — they have the best effort-to-conversion ratio and are fastest to produce well.

## 4. Structure by format

**Checklist:**
```markdown
# [Specific, benefit-driven title]
[1-2 sentence intro: who this is for and what it saves them from]

## [Section 1 name]
- [ ] Specific, actionable item
- [ ] Specific, actionable item

## [Section 2 name]
...

[Closing line connecting back to the real offer — not a hard pitch, just the natural next step]
```

**One-page guide:**
```markdown
# [Title]
[1-2 sentence framing]

## [Concept 1]
[2-4 sentences, concrete]

## [Concept 2]
...

[Closing line + natural next step]
```

**Template:** produce the actual fillable template content/structure, not a description of one, plus a short instructions block above it.

---

## 5. Companion assets

A lead magnet rarely stands alone. When useful, also produce (briefly — these have their own fuller structures elsewhere in `_skills/` and the `marketing` plugin if deeper versions are needed):
- **Landing page teaser copy** — headline + 2-3 sentences pitching the magnet itself, built to get the opt-in, not to sell the full product.
- **Delivery email** — short, warm, delivers the promised asset immediately, one soft next-step CTA toward `Business/[slug]/context/products.md`.

---

## 6. Quality bar

- Solves exactly one specific problem, stated plainly in the title.
- Usable in under ten minutes.
- Every item/section is specific to `Business/[slug]/context/audience.md` and `Business/[slug]/context/products.md`, not generic industry filler.
- Tone matches `Business/[slug]/context/brand-voice.md`.
- Connects naturally to the real offer without being a hard sell.
- If `Business/[slug]/context/` was incomplete, that's noted rather than papered over.
- Doesn't invent proof (client results, testimonials) that don't exist yet — check `Business/[slug]/context/products.md` for honesty flags.

## 7. Response behavior

**If the business isn't clear:** ask before building anything — see Section 1, step 0.

**If given only a topic:** pick the best-fit format from Section 3, state the assumption, and produce the complete asset rather than asking first.

**If asked for ideas only (not the full asset):** give 3-5 specific concepts (title + one-line description + why it converts) and stop for approval before building the full asset.

**Once the full asset is produced:** save it automatically to `Business/[slug]/examples/` per Section 8 (no need to ask "should I save this?" first), and confirm the save in your response with the file path (e.g. "Saved to `Business/[slug]/examples/2026-07-09_lead-magnet_[slug].md`").

## 8. Save Your Output

Once the lead magnet (and any companion assets) is finished, save it as a new file in `Business/[slug]/examples/` named `YYYY-MM-DD_lead-magnet_[short-descriptive-slug].md` — use today's real date (e.g. `2026-07-09_lead-magnet_moving-day-checklist.md`) if known at run time, otherwise fill in the actual send/creation date when saving. This is a universal convention across the content skills: `Business/[slug]/examples/` is the finished-copy archive every skill reads from first (see Section 1, step 6) and writes to on completion, so future runs — and other skills — have real, approved examples to calibrate against. Save automatically every time; don't ask permission first.

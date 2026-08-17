---
name: social-post-pack
description: >
  Produces one finished, ready-to-publish social post in a single run — hook, caption, hashtags, alt text, and an actual exported PNG graphic — by chaining copywriting, a virality grade, and image production instead of stopping at "visual direction." Reads brand voice, audience, products, and brand-board tokens from Business/[slug]/context/ at runtime rather than hardcoding any brand, and saves finished output to the business's social/, visuals/, and examples/ folders. Use when the user wants a post they can actually publish — "make me a post," "create a social post," "I need something to post today," or any single-post request where they expect a graphic and not just copy. For copy and written visual direction only, use social-creative-designer. For multi-slide carousels use carousel-post-designer, for a full week use weekly-content-plan, and for paid ads use ad-creative-designer.
---

# Social Post Pack

One request in, one publishable post out. This is the skill behind the menu's "Create a Social Post" card, and it exists because the old path stopped one step short: `social-creative-designer` produced excellent copy plus a written *description* of a visual, and the user still had to go make the graphic. This skill runs the whole chain.

**The deliverable is a file plus a copy block, not a description of one.** If you finish this skill without a PNG on disk or an explicit, honest statement of why one couldn't be made, you have not finished this skill.

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

**Confirm the business profile.** The active business was resolved once at the top of this skill — don't re-resolve or re-ask here. If no profile exists yet, stop and run `business-setup` first: content written against a placeholder context folder is generic filler and wastes the run.

Otherwise read, in this order:

- `memory.md` at the project root — active work and open threads
- `Business/[slug]/context/brand-voice.md` — tone, approved language, words to avoid
- `Business/[slug]/context/audience.md` — who this is for and how they describe their own problem
- `Business/[slug]/context/products.md` — what's actually being sold, so claims stay real
- `Business/[slug]/context/style-guides/social.md` — platform conventions, hashtag policy, emoji rules
- `Business/[slug]/context/brand-board.md` — hex colors, typography, logo path, imagery style
- `Business/[slug]/examples/` — already-approved posts; treat as voice calibration. Empty is fine, don't block.
- `Business/[slug]/social/content-calendar.md` — check what already went out so this post doesn't repeat last week's angle

## 2. Lock the inputs

You need five things:

| Input | Default if unstated |
|---|---|
| Topic or angle | Propose 3 one-line angles from their context and calendar, and let the user pick |
| Platform | Instagram (note the post also works cross-posted to Facebook) |
| Ratio | 4:5 — 1080×1350, the most feed real estate a single image gets |
| Visual style | Designed text card |
| Photo path | None |

**If this skill was reached through the `menu` skill, the spec form already collected these — do not ask again.** If it was invoked directly and inputs are missing, either render `menu`'s `assets/spec-widget.html` with these five fields, or ask for all of them in **one** message. Never a sequence of questions.

If the user says "you pick," pick and say what you picked in one line.

## 3. Write the copy

Follow `social-creative-designer`'s rules for structure and voice — this skill does not re-derive them. Produce:

- **Hook** — line one, the scroll-stopper. Carries the whole post.
- **Body** — 2–5 short paragraphs, one idea each, written to the audience's actual language.
- **CTA** — one, specific, matched to where the business can actually convert.
- **Headline** — the short line that goes *on the graphic*. Not the same as the hook; it has to survive at thumbnail size. Under 12 words, ideally under 9.
- **Hashtags** — per the business's `style-guides/social.md`. **Instagram's real cap is 5** — do not exceed it regardless of old habits.
- **Alt text** — one sentence, describes the image for screen readers. Not the caption again.

A post that could have been written about any business in any city is filler. Every one needs a specific angle and a real reason to stop scrolling.

## 4. Grade before you render

Run the copy through `post-grader`'s rubric — hook strength at 50%, plus curiosity, emotional charge, share-worthiness, voice match, polarity, platform fit.

**Revise until it scores 8/10 or higher.** Do this silently; don't narrate each pass. Rendering a graphic for weak copy just wastes the render. Report the final score in one line at the end.

If it's stuck under 8 after three passes, say so plainly and show the user the strongest version with the specific reason it's capped — usually the topic itself has no tension.

## 5. Render the graphic

**Follow the render ladder in `graphic-production-studio` Mode F.** It is defined once, there, and this skill does not restate it: Pillow first, Chromium only for layouts Pillow genuinely cannot do, honest failure last. Say which rung produced the file.

For this skill the ladder starts at the bundled `scripts/render_post_graphic.py`. Write a spec JSON from the business's `brand-board.md` and run it with whatever Python actually resolves in this session — try `python3`, then `python`, then `py`, and use the first whose `--version` really prints a version (on Windows `python3` can exist as a stub that fails when run):

```bash
python3 scripts/render_post_graphic.py spec.json out.png
```

Layouts: `editorial` (text card, or photo band on top), `photo-overlay` (full-bleed photo with a bottom scrim), `quote` (accent rule beside the headline). Every color, font, and logo path in the spec must trace back to `brand-board.md` — if that file is a placeholder, say so and fall back to clean neutral defaults rather than inventing a brand.

The renderer auto-shrinks the headline to fit its box, so text never overflows — but a headline that shrinks below ~40px is a signal the headline is too long, not that the renderer failed. Shorten the copy instead.

### When the post needs a photographic scene

This is a different intent, not a lower rung — decide it *before* rendering, not after a rung fails. If the post needs a photograph the business doesn't have, generate the scene with an image-generation tool (found by capability, never by a literal name), then composite the headline over it via the `photo-overlay` layout. If no such tool resolves, use a designed text card instead and don't remark on it.

**Never** use an AI-generated image to depict a real property, a real project, or a real person. For a property or construction business that is a factual misrepresentation, not a stylistic choice. Real work needs real photos — that's the business the user is in.

## 6. Deliver

1. **State the PNG's full path** — the file on disk is the deliverable (see Section 7). If this surface can also display the image inline, do that after the file is written; if it can't, don't mention it.
2. **Post the copy block** in the response as a clean, copy-pasteable unit: hook, body, CTA, hashtags, alt text. No commentary interleaved.
3. **One line of QA context:** the grade, the platform, the dimensions.

## 7. Save the output

Every finished post lands in the business's folder — this system builds a passive archive, not chat history.

| What | Where |
|---|---|
| Full copy | `Business/[slug]/examples/YYYY-MM-DD_social_[topic-slug].md` |
| PNG + spec JSON | `Business/[slug]/visuals/YYYY-MM-DD_social_[topic-slug].png` / `.json` |
| Calendar row | append to `Business/[slug]/social/content-calendar.md` |

Calendar row format: `| Date | Format | Channel | Summary | Status | File |`. In Dropbox mode there is no in-place append — fetch the live file immediately before editing, then delete and recreate at the same path. Never append from an earlier read.

**Delivering the rendered PNG.** Writing the file into the workspace *is* the delivery, not a step before it.

1. **Write it to `Business/[slug]/visuals/`** as `YYYY-MM-DD_social_[topic-slug].png`, and write the spec JSON beside it with the same filename stem. State the full path in your reply. That file is what the business keeps; the conversation is not storage.
2. **Confirm the write before you report it.** List the folder or check the file exists. Never report a `visuals/…png` path you did not verify — a fabricated save confirmation is worse than an honest failure.
3. **Showing the image in the conversation is a surface-dependent extra.** If this surface can display or attach the file, do it *after* the file is written, and still give the path in the same turn. If it can't, say nothing about it — the saved file is already the deliverable. Do not call a tool to hand the file over unless you have confirmed that tool exists in this session; assume none does.
4. **In `storage_mode: dropbox`, binaries do not go through the connector** — `create_file` is text-only. Write the spec JSON through the connector so the image can be re-rendered, keep the PNG in the local working folder, and say plainly that the image itself did not sync and where the source landed. Never list a Dropbox `visuals/…png` path the connector could not write.

## 8. Offer the next step, once

End with a single line offering to schedule it via `post-scheduler`. One line. Don't sell it, don't list the platforms, and don't schedule anything without an explicit yes.

## 9. Quality bar

Before delivering, check:

- [ ] The hook works with zero context — no "As we mentioned last week."
- [ ] Every claim traces to `products.md`. No invented stats, awards, or timelines.
- [ ] The graphic headline is legible at thumbnail size.
- [ ] Colors and logo trace to `brand-board.md`, or the fallback was disclosed.
- [ ] Hashtags are within the business's policy and Instagram's 5 cap.
- [ ] Alt text describes the image, not the caption.
- [ ] The post scored 8+, or the cap was explained.
- [ ] The file was actually written to disk and actually sent.

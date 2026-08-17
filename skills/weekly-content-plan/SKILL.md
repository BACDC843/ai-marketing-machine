---
name: weekly-content-plan
description: >
  Produces a full week of ready-to-post social content — one on-brand post per day for 7 days, on whichever platforms the business actually uses — graded against the post-grader rubric and revised until every post scores 8/10+, exported as branded graphics, and saved to Business/[slug]/social/. Reads brand-voice.md, audience.md, products.md, style-guides/social.md, and brand-board.md from Business/[slug]/context/ at runtime — never hardcodes any voice or visual identity. Use whenever the user asks for a week of content, a content batch, "give me a week of posts," "fill out next week's calendar," "post consistently," or wants social content produced and graded in bulk rather than one post at a time. The batch counterpart to social-creative-designer and post-writer — use one of those for a single post.
---

# Real Estate Weekly Content Creation

A single post is easy to get right one at a time. A week of them is a different problem: seven days need to not repeat each other, need to rotate through the business's real content pillars and audience segments, need to actually clear a quality bar instead of just existing, and need to land somewhere a human can review them before anything goes live. This skill runs that whole batch — draft, grade, revise, visualize, save, present, and (on request) schedule — for a real-estate or builder business, using nothing but that business's own documented brand.

It composes rather than duplicates: hook mechanics come from `post-writer`, the grading rubric comes from `post-grader`, the visual pipeline's brand-token approach comes from `graphic-production-studio`, and the Blotato mechanics come from `post-scheduler`. Read those four skills' `SKILL.md` files if you need the full detail behind any single step below — this skill sequences them into one weekly batch, it doesn't re-derive their logic.

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

The active business is already resolved. Before drafting anything:

0. **Confirm the business profile.** The active business was resolved once at the top of this skill — don't re-resolve or re-ask here. If no profile exists yet, stop and run `business-setup` rather than writing against an empty context folder.
1. Read `Business/[slug]/context/brand-voice.md` — tone, vocabulary, hook templates, CTA toolkit, do's/don'ts. This is the actual voice you're writing in, not a generic one.
2. Read `Business/[slug]/context/audience.md` — segments/archetypes to rotate across the week, pain points, decision triggers.
3. Read `Business/[slug]/context/products.md` — real services, budget signals, honesty flags (pre-revenue or pre-case-study businesses need proof-point language handled carefully — don't invent results).
4. Read `Business/[slug]/context/style-guides/social.md` — this tells you which platforms are actually real for your business (don't assume every platform — many local businesses are Facebook + Instagram only), each platform's real length/hashtag/tone conventions, the documented posting cadence, and the content-pillar rotation.
5. Read `Business/[slug]/context/brand-board.md` — color palette, typography, layout patterns, logo rules. This drives every graphic in Section 6; never invent brand colors that aren't in this file.
6. Read `Business/[slug]/social/content-calendar.md` — everything already published or drafted in roughly the last 60 days. The whole point of a fresh week is that it isn't a rerun of last month; skim topics and hooks already used and steer around them.

If any of these files is a thin placeholder, say so plainly and proceed on the best real material available rather than inventing brand facts to fill the gap — this matches the standard every other skill in this project holds itself to.

---

## 2. Decide the week's shape before writing anything

**Platforms**: only the ones `style-guides/social.md` and `audience.md` say your business actually uses. Don't add LinkedIn or TikTok because they're common elsewhere — add them only if the business's own docs name them.

**Cadence honesty**: `style-guides/social.md` almost always documents a real posting frequency (e.g. "3-5 IG posts/week, 1-2 FB posts/week") that's lower than "one post every day on every channel." Build the full 7-day batch anyway — it's useful as inventory — but state the business's actual documented cadence next to it, explicitly, so the user understands this is a bank to draw from, not a mandate to publish daily on every channel. Don't silently drop days to match the lower cadence unless asked; the value of a week of content is having more ready than you need.

**Pillar and archetype rotation**: pull the content pillars and audience archetypes straight from `brand-voice.md` / `audience.md` (pillars are typically shapes like Project Reveals, Behind-the-Scenes, Education & Authority, and Social Proof; archetypes are the business's own named buyer personas). Assign each of the 7 days a distinct pillar + archetype pairing, cross-checked against `content-calendar.md` so no topic repeats a recent post. A week that's six education posts and one lifestyle post fails this even if every individual post is good — variety across the week is part of the deliverable.

**CTA distribution**: if `brand-voice.md` documents a CTA-type mix (e.g. "~50% save/share, ~25% comment/DM, ~15% link in bio, ~10% soft/no-CTA"), spread the week's CTAs to roughly match it rather than reusing the same CTA seven times.

---

## 3. Draft each day, voice rules baked in from the start

For each day, for each real platform: write hook, body, and CTA using `post-writer/SKILL.md`'s hook-pattern and CTA-pattern guidance, but the actual voice, vocabulary, and CTA toolkit come from the business's `brand-voice.md`, not `post-writer`'s generic defaults — a business's own documented hook templates and CTA toolkit always win over generic ones when both exist.

Apply the universal voice rules as you write, not as an afterthought:
- Zero em dashes
- Contractions used
- Numbers as digits
- Active voice throughout
- Zero filler words: really, very, just, basically, literally, actually, simply
- No filler openers: "in today's world," "let me tell you," "the truth is"

**Before grading, actually scan the drafted text for these** rather than eyeballing it — write a short script (or use grep/search) that checks every caption for the banned words and em dashes. A single stray "actually" slipped past a visual read-through the last time this ran live; a real scan catches what a read-through misses.

Match each platform's real length convention from `style-guides/social.md` (e.g. Instagram short-to-medium with a hook in the first ~125 characters, Facebook 100-250 words) — not a generic platform default. Measure actual character and word counts after drafting (script it, don't estimate) and report the real numbers.

---

## 4. Grade every post, loop until it clears 8/10

Apply `post-grader/SKILL.md`'s exact rubric to every single post (hook strength 50%, curiosity & specificity 10%, emotional charge 10%, share-worthiness 10%, voice match 10%, polarity 5%, platform fit 5%; each voice-rule violation from Section 3 subtracts 0.5, capped at -3).

If a post scores under 8, revise it — almost always by strengthening the hook, since it's half the score — and re-grade. **Document the loop honestly**: if a post needed a revision to clear 8, say what the first draft scored, what was weak about it, and what changed. Don't silently present only the final version as if it were right the first time; a visible revision loop is evidence the grading is real, not rubber-stamped. If a post still can't clear 8 after two honest revision attempts, say so plainly and present the best version with its real score rather than inflating the number to hit the target.

---

## 5. Generate a visual for each day

One graphic per day is enough — the same image can serve both platform versions of that day's post, since they're the same underlying photo/design choice with different caption lengths on top.

1. Check `Business/[slug]/visuals/` for existing assets and naming conventions already in use for your business, per `graphic-production-studio/SKILL.md` Section 1.
2. Every color, font, and layout choice traces back to `Business/[slug]/context/brand-board.md` — never invent brand values.
3. Decide per day whether a real photo exists for the topic. Most days in a forward-looking weekly batch won't have one (there's no finished project to photograph for a hypothetical scenario), so the default path is one of:
   - **AI-generated photography**, disclosed plainly in the saved post file and stamped on the image itself (the bundled script's `photo_disclosure: "ai-generated"` config does this automatically) — use when the business's brand-board.md photography direction and existing asset library lean photographic.
   - **A pure typographic editorial card** (headline + body baked onto a solid/gradient brand-color background, no photo at all) — use when that fits the business's existing visual language better, or when no good AI photo generation path is available in the current session.
   Say which path was used for each day; never let a synthetic photo pass as a real project photo.
4. **Export with the bundled Pillow script** (`scripts/flatten_editorial_post.py`), not a Playwright/HTML pipeline. Pillow is rung 1 of the render ladder defined in `graphic-production-studio` Mode F — no browser, no network, works on every platform. Only reach for Chromium if a layout genuinely needs something Pillow cannot do; its absence is "not applicable", not a failure. Build one JSON config per day (see the script's own docstring and `CONFIG_EXAMPLE` for the exact shape — canvas size, layout, brand hex values pulled from `brand-board.md`, headline/body/CTA copy, and `photo_disclosure`), then run `flatten_editorial_post.py <config>.json` with whatever Python resolves in this session — try `python3`, then `python`, then `py`, and use the first whose `--version` really prints a version. Confirm the output file actually exists on disk before calling it done.

---

## 6. Save everything

**Per-post files**: `Business/[slug]/social/[date]_single-post_[topic-slug].md`, one file per day, matching the existing per-post convention already in use for your business (check a recent file in that folder for exact section headers if unsure). Each file includes: hook, full caption per platform, hashtags used, CTA + CTA-type label, real character/word counts, the post-grader scorecard (including any revision-loop note from Section 4), and an **Assumptions/flags section** for anything fictional, unverified, or AI-generated (see Section 10).

**The day graphics**: write all seven rendered PNGs to `Business/[slug]/visuals/`, each with its re-renderable source (the per-post spec JSON) beside it under the same filename stem. State the paths, and confirm the writes before reporting them — never list a `visuals/…png` path you did not verify. Displaying them in the conversation is a surface-dependent extra: do it after the files are written if this surface supports it, and say nothing about it if it doesn't. Do not call a tool to hand files over unless you have confirmed it exists in this session; assume none does. In `storage_mode: dropbox` the PNGs cannot cross the connector — write the spec JSON through it, keep the images in the local working folder, and say so plainly. Do not finish a run with seven graphics stranded nowhere.

**Content calendar**: append one row per day to `Business/[slug]/social/content-calendar.md` (in Dropbox mode there is no in-place append — fetch, add rows, delete and recreate at the same path), matching that file's existing columns. Status starts as "Drafted" (or "Scheduled..." if Section 8 ran too).

**Style-guide corrections**: if executing this skill surfaces a real, verified correction to the business's own documented conventions (the way scheduling once revealed Blotato's actual 5-hashtag Instagram cap versus a business doc's higher documented range), write that correction into the relevant `style-guides/` file with a dated note, not just into this run's output — otherwise the same gap gets rediscovered next time.

---

## 7. Render the week as a Claude Artifact

This is the primary human review surface — the user needs to see and approve a week of content before it goes anywhere, and a wall of markdown files is a poor way to do that.

**Surface check first.** Rich inline rendering is not available everywhere, and you cannot observe whether it worked. **Always build and save the HTML file** to `Business/[slug]/social/` and state its verified path — that file is the durable review surface. Then post a compact plain-text week summary in chat: one line per day with the day, pillar, platform, the first line of the caption, and its score. That summary is what the user approves from on a phone. Render it inline as well only if this surface supports it; do not block the run waiting for a surface that isn't there.

Load the `artifact-design` skill and treat this as the "polished working document" treatment (a content calendar plus grading report), not a marketing landing page — real typographic hierarchy and considered spacing, not a flashy hero. Ground every color and type choice in the business's actual `brand-board.md` tokens (their real navy/gold/serif system, or whatever theirs is) rather than a generic AI-artifact look — this is the single easiest way for this to feel like it belongs to the business instead of looking like every other AI-generated page. Design for both light and dark theme. Show, per day: the pillar/archetype pairing, each platform's full caption (with a copy-to-clipboard control), hashtags, CTA type, real char/word counts, and the score breakdown — including any revision-loop note from Section 4, since that's evidence the grading was real. Save the HTML to the path above and state it, then post the plain-text week summary. Render or publish it inline as well only where this surface supports it. Never claim to have published a link that was never rendered.

---

## 8. Optional: schedule via Blotato

**Only when the user explicitly asks** — "schedule these," "post these to Blotato," naming specific days/times, or similar. Drafting a week and scheduling a week are two different requests; never auto-schedule after drafting.

Read `references/blotato-batch-scheduling.md` for the full batch-scheduling workflow — it covers matching the business's platforms to Blotato accounts, uploading local graphics via presigned URLs, the confirmed real Instagram 5-hashtag cap (which can be lower than a business's own style-guide document), writing returned post IDs back into both the per-post files and the content calendar, and surfacing a cadence-mismatch flag when the requested schedule exceeds the business's documented posting frequency.

---

## 9. What NOT to do

- Don't repeat a topic, hook, or angle from the last ~60 days of `content-calendar.md`.
- Don't assign every day the same content pillar or the same CTA type — variety across the week is part of the deliverable.
- Don't grade leniently or present a sub-8 post as if it cleared the bar.
- Don't skip the actual filler-word/em-dash scan and rely on a visual read-through — it misses things.
- Don't invent brand colors, fonts, or voice that aren't in the business's real `context/` files.
- Don't let a synthetic (AI-generated) photo pass as a real project photo without disclosure.
- Don't fabricate a business testimonial or quote and present it as real.
- Don't state an unverifiable regulatory, legal, or permitting-timeline claim as settled fact — flag it for human confirmation instead (see Section 10).
- Don't auto-schedule. Drafting and scheduling are separate requests.
- Don't silently exceed a business's documented posting cadence when scheduling — say so.

---

## 10. Never fabricate

- **No invented testimonials.** If a post wants social proof, use a process/philosophy angle ("the one question we ask every business") instead of a fake attributed quote.
- **No real addresses or project specifics** unless the user supplied them. Fictional-but-realistic archetype scenarios are fine exactly when the business's own `brand-voice.md` says that pattern is acceptable (check for language like "use real project scenarios and fictional-but-realistic homeowner stories") — and even then, say plainly in the post's Assumptions/flags section that the scenario is illustrative, not a real job.
- **No unverified regulatory/legal/permitting claims stated as fact.** If a post needs a specific number (a timeline, a fee, a review-board turnaround) that isn't confirmed in the business's context files, use it if it's realistic and useful for the hook, but flag it explicitly in that post's saved file as needing human confirmation before publishing — don't quietly hope it's close enough.
- **No AI-generated photography presented as a real project photo.** Disclose it, both in the saved file and (via the bundled script's `photo_disclosure` field) stamped on the image.

---

## 11. Quality bar

- Every brand fact (voice, audience, palette, cadence) traces back to the business's real `Business/[slug]/context/` files — nothing invented.
- Seven days, seven distinct pillar/archetype pairings, no repeated topic from recent calendar history.
- Every post scores 8/10 or higher on the real post-grader rubric, with an honest revision-loop trail where one was needed.
- Real, measured character/word counts against the business's actual style-guide targets, not generic platform defaults or estimates.
- One graphic per day, every brand token traceable to `brand-board.md`, disclosed honestly if AI-generated or purely typographic.
- Fabrication-free: no fake testimonials, no unverified claims stated as settled fact, no undisclosed synthetic photography.
- Everything saved to the right place (`social/`, `content-calendar.md`) and put in front of the user in a reviewable form before anyone is asked to approve or schedule it — the saved HTML file plus the plain-text week summary, rendered inline where the surface allows. The requirement is that the week was *reviewable*, not that an artifact rendered.

## 12. Response behavior

**If the business isn't clear:** ask before drafting anything — see Section 1, step 0.

**After drafting and saving (Sections 3-7):** report the average score, how many posts needed a revision loop, the business's real documented cadence next to the 7-day batch, and any open flags from Section 10 — then link the Artifact (or, off desktop, point at the delivered file and the text summary) and ask whether the user wants to schedule any or all of it via Blotato, or adjust specific days first.

**If asked to schedule:** follow Section 8 / `references/blotato-batch-scheduling.md`, and repeat any still-open flags from Section 10 in the scheduling confirmation — scheduling a flagged post doesn't resolve the flag.

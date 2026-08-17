---
name: website-portfolio-report
description: >
  Turns a business's website URL into a complete marketing portfolio in one run: Firecrawl-scrapes the
  site (copy AND visual brand — real hex colors, fonts, logo), builds brand context, runs the full
  skill portfolio (campaign strategy, blog post + SEO brief, 3+ social posts with rendered graphics,
  carousel, lead magnet, ad concept), QAs it all with brand-review, and compiles one polished Word
  (.docx) report with the visuals embedded. Use whenever the user drops in a website URL and wants
  "the full portfolio," "a marketing package," "a pitch report," "run everything on this site," a
  marketing audit with sample content, or a sample content package for a prospect. Two modes: prospect
  (no business folder — the report IS the deliverable) and profile (also
  builds the business's Dropbox project via business-setup). For a single piece of content, use the
  specific content skill instead.
---

# Website → Portfolio Report

One input (a website URL), one deliverable (a Word report a business owner can hold): brand capture, a
full batch of real, on-brand sample content — including at least three social posts with actual rendered
graphics — and an honest account of what's real, what's inferred, and what's still needed.

The report this skill produces is only as persuasive as it is *credible*. A business owner knows their own
brand instantly — one invented statistic, one made-up testimonial, one wrong color, and the whole
portfolio reads as generic AI output. Every step below exists to keep the output specific and true.

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

## 0. Determine the mode

- **Prospect mode** (default when no `Business/[slug]/` folder exists for this business, or the
  user frames it as a pitch/audit/prospect): everything happens in the session's local workspace; the
  .docx report is the deliverable. No Dropbox folders are created — don't scaffold a business project for
  a business that hasn't signed.
- **Profile mode** (the business already has a profile, or the user wants one built): run
  `business-setup` first if no context folder exists, then this skill. All markdown/HTML outputs sync
  to the business's typed output folders in Dropbox as well as going into the report — the blog post and
  its content brief to `Business/[slug]/seo/` and `examples/`, social posts and the carousel to
  `Business/[slug]/examples/` (with `social/content-calendar.md` rows), the campaign strategy to
  `Business/[slug]/examples/`, and any rendered graphics to `Business/[slug]/visuals/` — same destinations
  each of those content types' own skill would use.

If genuinely ambiguous and the user is present, ask — one question, both modes named. If unattended,
default to prospect mode (it's non-destructive) and say so in the report.

Set up a local working folder: `[workspace]/portfolio-runs/[site-slug]/` with subfolders `context/`,
`content/`, `visuals/`, `report/`.

## 1. Capture — scrape before you write anything

**Check for supplied assets first.** In profile mode, check `Business/[slug]/context/brand-board.md` for
already-captured brand assets (logo URL, palette, fonts) before scraping — if the business was already
onboarded, don't redo work `business-setup` already did. If nothing's captured yet, ask the user
directly whether they have logo files, a brand kit, or sample posts to supply; real supplied assets
always beat scraped ones. In prospect mode, check whether the user attached anything to the conversation.

**Firecrawl scrape (the load-bearing step).** Load the Firecrawl tools via ToolSearch if deferred, then:

1. `firecrawl_scrape` with `formats: ["branding", "screenshot"]` — returns real hex colors, font families
   and sizes, button/component styles, logo URL, favicon, og:image, plus a screenshot. This is the visual
   identity capture that text-only fetching can't do.
2. `firecrawl_scrape` with `formats: ["markdown"]` on the homepage, and on the 2-4 most content-bearing
   pages (about/bio, services, testimonials/reviews if linked) — this is the copy, positioning, offers,
   and proof material.
3. Supplement with 1-2 targeted web searches ("[business name] reviews", "[owner name] interview") —
   third-party material often surfaces proof points and voice the site itself doesn't have.

**Honesty rules for captured data** (these carry through every downstream step):
- Captured palette/fonts are **live-site values, not a business-confirmed brand system**. Label them that
  way. If CDN hostnames reveal a templated platform (Sierra Interactive, kvCORE, Placester, Squarespace,
  Wix...), flag that the palette may be a theme default and needs confirming.
- If two sources conflict on a claim (a ranking, an award, a stat), never merge or pick silently — carry
  the conflict forward as an explicit open question and use only unambiguous proof in content.
- No invented pricing, testimonials, credentials, or team-member detail. Missing is stated as missing.
- If Firecrawl is unavailable, fall back to WebFetch (text only), leave visual identity explicitly
  uncaptured, and note it in the report — don't invent a palette to compensate.

## 2. Build the working context

Write the standard four context files into the run's `context/` folder (same shapes as
`Business/_template/context/`): `brand-voice.md`, `audience.md`, `products.md`, `brand-board.md` — each
with a source note. In profile mode these live in (or update) `Business/[slug]/context/` in Dropbox; in
prospect mode they stay local. Thin files beat padded files: two confirmed audience segments honestly
described outproduce six invented personas.

## 3. Run the portfolio

Produce this content set, each piece following its named skill's own instructions and reading the
context folder from step 2. Run independent pieces as parallel subagents when available (pass each one
the context folder path and the honesty rules from step 1); otherwise produce them sequentially.

| Piece | Skill | Notes |
|---|---|---|
| Campaign strategy overview | campaign-plan | The organizing spine — pick a real strategic angle from the audience/products files, not "increase engagement" |
| Blog post + SEO content brief | ai-search-blog-writer | Topic must pair a real audience segment with a real offer/CTA found on the site |
| **3+ social posts** | social-creative-designer | Different platforms AND different angles/segments — three variations of one hook is one post, not three |
| Carousel (multi-slide) | carousel-post-designer | Distinct angle from the social posts |
| Lead magnet | lead-magnet | Honest-assessment rule applies: if the site's existing tools ARE the real lead magnets, build something that supports them, or say a new one isn't warranted |
| Ad concept (brief + creative) | ad-creative-brief + ad-creative-designer | Mark contingent/on-hold unless paid is a confirmed active channel |

Every piece carries the step-1 honesty rules. Anything channel-contingent (paid, email) is labeled as
proposed, never as running.

## 4. Render the visuals (minimum 3)

Each of the 3+ social posts gets a real rendered graphic — not just "visual direction" text:

1. Build a self-contained HTML card (default 1080×1350) per post in `visuals/`, using the captured
   palette and fonts from step 1 (import Google Fonts when the captured fonts are Google-hosted).
   Include a small, visible disclosure badge on the canvas: "Live-site palette — pending brand
   confirmation" (or "Placeholder — no brand assets captured" in the fallback case). The badge is a
   feature, not a blemish — it shows the business/prospect you don't fake brand systems.
2. Render each one following the render ladder in `graphic-production-studio` Mode F — defined once
   there, not restated here. Say which rung produced the files:
   a. `scripts/render_post_graphic.py` (Pillow — no browser, no network), bundled in this skill's own
      folder. The default, and the only rung that works on every platform. Invoke Python as whatever
      resolves in this session: try `python3`, then `python`, then `py`, and use the first whose
      `--version` really prints a version — an existence check alone picks a Windows stub that fails.
   b. `node scripts/render_graphic.js <in.html> <out.png>` — only for layouts Pillow genuinely cannot do.
      Never run `playwright install`. If this throws `MODULE_NOT_FOUND` for `playwright`, or Chromium
      isn't present, that is "not applicable", not a failure — stay on rung (a) without remarking on it.
   c. Only if Pillow itself is unavailable: proceed with fewer visuals, say so explicitly in the report,
      and never present a missing graphic as a design choice.
3. Look at each rendered PNG (Read the image) before accepting it — check text fits, contrast works,
   nothing overflows. Fix and re-render, don't ship a broken card.

No AI-generated photorealistic property/people imagery standing in for real photos — typographic cards
are honest; fake photos aren't.

## 5. QA before compiling

Run `brand-review` across the whole batch (content + visuals + the context files' honesty flags). Fix
what it finds *before* the report is built — the report should embed corrected content, with the QA
summarized inside it. A finding rate of zero across 10+ pieces is suspicious; check the review actually
engaged rather than rubber-stamped.

Two hard-won operational notes: (1) if the QA runs as a subagent and dies mid-pass (rate limits,
session caps), check the run folder before re-spawning — it may have already written its report and
applied fixes; finish the remainder inline rather than paying for a full second pass. (2) If QA edits
any copy that a graphic was rendered from, the PNG is now stale — diff the card specs against the
rendered HTML and re-render anything that changed. Also audit the *context files themselves*: if a
capture note asserted an inference as fact (e.g., a posting cadence extrapolated from two data points),
downstream QA will wrongly "verify" content against that bad note. Sources can be wrong too.

## 6. Compile the Word report

**Only now** — with all content finished and QA'd — Read the docx skill's SKILL.md and follow it to build
the report. Structure:

1. **Cover** — business name, "Marketing Portfolio", date, prepared-by (the user's agency).
2. **Executive summary** — one page: what was captured, what was produced, the 2-4 most important open
   questions/decisions (the honesty flags, front and center — this is what separates this report from
   generic AI output).
3. **Brand snapshot** — captured palette (rendered as color swatches), fonts, logo, site screenshot,
   with the live-site-vs-confirmed caveat stated plainly.
4. **Strategy** — the campaign overview.
5. **Sample content** — every piece in full, one section per piece; each social post section embeds its
   rendered PNG at readable size.
6. **Quality review** — brand-review summary: what was checked, what was found, what was fixed.
7. **What we'd need from you / next steps** — the open items (real logo files, photo assets, claim
   confirmations, channel decisions) framed as the beginning of an engagement, and — in prospect mode —
   a short closing paragraph positioning the user's agency as the team that executes this.

**Delivering the report.** Write the `.docx` into the run folder (`portfolio-runs/[site-slug]/`) or, in
profile mode, into `Business/[slug]/examples/`, and state its full path. Confirm the write before you
report it — never report a path you did not verify. Attaching or previewing it in the conversation is a
surface-dependent extra: do it after the file is written if this surface supports it, and say nothing
about it if it doesn't. Do not call a tool to hand the file over unless you have confirmed that tool
exists in this session; assume none does. In `storage_mode: dropbox` the `.docx` is binary and cannot
cross the connector — sync the markdown/HTML sources through it instead and say plainly where the
`.docx` itself landed. In profile mode also add content-calendar rows. If the user asked for PDF,
convert the finished `.docx` rather than authoring twice.

## Quality bar

- The report would survive the business owner reading it: no invented facts, no merged conflicting
  claims, no fake brand system presented as real, every proof point traceable to a source.
- The 3+ social posts are genuinely distinct (different segment, angle, or platform mechanics) and each
  PNG was actually viewed and verified after rendering.
- Cheap-to-fix realities are handled: dated filenames use the real current date; the run works even when
  Firecrawl or subagents are unavailable (degrade, note it, continue).
- Time expectation: a full run is substantial (10+ pieces, renders, a compiled document). Say so up
  front, keep a task list, and deliver the report even if one non-essential piece fails — note the gap
  rather than blocking the deliverable.

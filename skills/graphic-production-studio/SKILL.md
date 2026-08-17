---
name: graphic-production-studio
description: >
  Shared visual-production engine — turns approved copy from social-creative-designer, carousel-post-designer, ad-creative-designer, lead-magnet, ai-search-blog-writer, or repurposing-to-newsletter into an actual designed visual asset: a design brief, an image-generation-ready JSON prompt, or an exported PNG. Reads brand tokens (colors, typography, logo rules, layout patterns) from Business/[slug]/context/brand-board.md at runtime rather than hardcoding any design system. Use whenever the user asks to actually design, export, render, or generate the graphic for a post, carousel, blog header, lead magnet, ad, or newsletter — not just get copy or "visual direction" text. If no copy exists yet, use the relevant content skill first — this skill designs from finished copy, it doesn't originate messaging.
---

# Graphic Production Studio

Every content skill in this project can describe what a visual *should* look like. This skill is the one that actually builds it — a design brief specific enough to hand to a designer, a JSON prompt ready for an image generator, or an exported PNG file. It doesn't write headlines or body copy; it takes copy that's already been approved and turns it into pixels, using the requesting client's real brand system every time.

Do not invent a brand identity. Every color, font, and layout instruction in this skill's output must trace back to `Business/[slug]/context/brand-board.md` — if that file is a placeholder, say so and fall back to clean, neutral defaults rather than making up a fake brand.

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

## 1. Determine the business, then read their brand context

The active business is already resolved. Before doing anything else:

0. **Confirm the business profile.** The active business was resolved once at the top of this skill — don't re-resolve or re-ask here. If no profile exists yet, stop and run `business-setup` rather than writing against an empty context folder.

1. Read `Business/[slug]/context/brand-board.md` — color palette, typography, logo rules, layout patterns, component tokens, and any social/carousel canvas specs already defined. This is the mandatory core input for every output mode below.
2. Read `Business/[slug]/context/brand-voice.md` — tone words that should inform mood, scene description, and photography direction, not just copy.
3. Read `Business/[slug]/context/style-guides/visuals.md` — photography use/avoid direction, and critically, whether AI-generated graphics are treated as the default or as an exception for your business (some brands explicitly want real photo/video as the default and generated graphics only for announcements — respect that distinction, don't apply one business's visual policy to another).
4. Check `Business/[slug]/visuals/` for existing assets already produced for your business. If any exist, use them as a consistency reference — confirm the same brand tokens, canvas dimensions, and naming pattern are being reused, and avoid accidentally duplicating a slide number or asset name already used for your business. This folder may be empty for a business with no history yet — that's fine, don't block on it.

**If `brand-board.md` is still an unfilled placeholder,** say so plainly, then use clean, neutral, high-contrast defaults (dark text on white/warm-white, one accent color, a simple sans-serif) rather than inventing brand colors or fonts that aren't real. Never let a placeholder silently produce output that looks like a finished brand decision.

---

## 2. Asset types this skill produces

| Asset type | Typically requested from | Default canvas (unless `brand-board.md` overrides) |
|---|---|---|
| Single social graphic | `social-creative-designer` | 1080×1080px (1:1) or 1080×1350px (4:5) |
| Carousel slide set | `carousel-post-designer` | 1080×1350px (4:5), N slides |
| Blog header / social-share image | `ai-search-blog-writer` | 1200×630px (standard Open Graph/social-share size) |
| Lead magnet cover + interior pages | `lead-magnet` | 1275×1650px (US Letter portrait @150dpi) unless the asset is a single-page checklist, which can use a social-graphic canvas instead |
| Ad creative graphic | `ad-creative-designer` | Per that skill's Meta spec table — 1080×1080, 1080×1350, or 1080×1920 depending on placement |
| Newsletter header banner | `repurposing-to-newsletter` | 600×200px (standard email-safe width) |

If `Business/[slug]/context/brand-board.md` defines its own dimensions for a given asset type (e.g., a business's documented carousel specs), those take precedence over the defaults in this table.

When a source skill hands off work here, it should pass: the asset type, the finished copy (headline/body/CTA per slide or page), and any format constraints already established (e.g., Meta's character/dimension limits from `ad-creative-designer`). This skill doesn't re-derive strategy or re-write copy — it designs what's already been approved.

---

## 3. Mandatory image rule

By default, every visual asset should carry a real photorealistic image anchor, not a text-only card — unless `Business/[slug]/context/style-guides/visuals.md` says otherwise for your business, or the user explicitly asks for a text-only or graphic-only treatment. Some brands explicitly want generated graphics treated as the *exception*, reserved for announcements — check this per business rather than assuming a photorealistic default fits everyone.

**If a slide/page's image is AI-generated rather than a real photo, disclose that plainly.** Never let a business-facing deliverable imply a real photo of a real project, product, or person unless it is one.

---

## 4. Output modes

### Mode D — Design brief

Use when the user wants a brief to hand to a human designer or to Claude Design rather than finished export-ready output. Output:

1. Overall creative direction (tie back to the source copy's angle and the business's brand voice)
2. Color palette — pulled directly from `Business/[slug]/context/brand-board.md`
3. Typography direction — heading/body fonts and weights, from `brand-board.md`
4. Layout system — which named layout pattern(s) from `brand-board.md` fit this asset type, or a described pattern if none exist yet
5. Per-slide/per-page visual instructions — scene description, mood, lighting, what the image should show
6. Exact text placement guidance
7. What to avoid (pulled from `style-guides/visuals.md`)

Make the brief specific enough that whoever builds it doesn't have to guess or invent brand details.

### Mode E — Graphic JSON prompts

Use when the user wants image-generation-ready prompts (e.g. for Higgsfield's `generate_image` or a similar tool). Return one JSON object per slide/page using the template in Section 5. Pull every brand value from `Business/[slug]/context/brand-board.md` — never invent brand values that aren't in context.

### Mode F — PNG export

Use when the user wants an actual image file rather than a brief or a prompt.

**The render ladder — this is the one definition. Every skill in this plugin that exports an image follows it; none of them restate it.** Work down, stop at the first rung that succeeds, and **say which rung produced the files**.

#### Rung 1 — Pillow (the default, and the only rung that works everywhere)

Use this skill's own bundled `scripts/render_post_graphic.py`. No browser, no network, no Playwright — if Pillow imports, this works. Layouts: `editorial` (text card, or photo band on top), `photo-overlay` (full-bleed photo with a bottom scrim), `quote` (accent rule beside the headline). Write a spec JSON from `brand-board.md` and run `scripts/render_post_graphic.py spec.json out.png`.

The same renderer is bundled into `social-post-pack` and `website-portfolio-report` so each skill can resolve it from its own folder — a fix to one must be applied to all three.

Invoke Python as whatever actually resolves in this session. Try `python3`, then `python`, then `py`, and use the first whose `--version` **actually prints a version**.

**Checking that the command exists is not enough.** On Windows, `python3` exists as a Microsoft Store alias that resolves on a path check and then fails when run — so a "does this command exist" probe picks the one interpreter that cannot work. Run it and read the output. Do not hardcode one and report a failure that is really a naming difference.

Every colour, font, and logo path in the spec must trace back to `brand-board.md`. If that file is still a placeholder, say so and use clean neutral defaults rather than inventing a brand.

#### Rung 2 — Chromium, only for layouts Pillow genuinely cannot do

Overlapping type, real web fonts, complex grids, multi-slide carousel tracks. **Probe before launching; never assume.**

**Chromium being absent is "not applicable", not "failed."** Fall to Rung 1 without asking and without apologising — an image still gets produced, so this is not a degraded outcome worth narrating.

The recovery steps below are **Linux-only**. On Windows or macOS, skip Rung 2 entirely rather than working through them and reporting a failure:

  **Step 1 — check for a pre-installed browser:** `ls -la /opt/pw-browsers/chromium`. If it resolves (a symlink into a `chrome-linux/chrome` binary), launch with the explicit path — `p.chromium.launch(executable_path="/opt/pw-browsers/chromium")` — and skip `playwright install` entirely.

  **Step 2 — if that path does NOT exist,** and the session has network access, install it:
  ```bash
  pip install playwright --break-system-packages
  python3 -m playwright install chromium     # NOT --with-deps: sudo/apt is blocked for a non-root user and that flag fails outright
  ```
  Then launch normally (`p.chromium.launch()` with no `executable_path`).

  **Step 3 — if the downloaded Chromium fails to start on a missing shared library** (observed: `libXdamage.so.1`), fix it without root:
  ```bash
  apt-get download libxdamage1        # works unprivileged, unlike apt-get install
  dpkg-deb -x libxdamage1*.deb /tmp/libs
  export LD_LIBRARY_PATH=/tmp/libs/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
  ```

#### Rung 3 — honest failure

Only reachable if Pillow itself is unavailable. Deliver the copy, the design brief (Mode D), and the spec JSON (Mode E), and say in one plain sentence that no image could be produced and why. **Never describe a graphic as if it exists.** `render_post_graphic.py` exits `3` when Pillow is missing; the fix is `pip install Pillow`, and saying so is more use to the customer than a generic failure.

**Build notes for Rung 2:**

- Build a fully self-contained HTML file (inline CSS/JS) sized to the asset type's canvas from Section 2, unless `brand-board.md` specifies different dimensions.
- Use Python (`Path.write_text()`) to write the HTML file, not shell heredocs — shell interpolation can corrupt `$`, backticks, and embedded SVG/CSS.
- **Sourcing and downloading images:** if imagery comes from an AI image generator (e.g. Higgsfield's `generate_image`), don't leave the HTML pointing at the generator's hosted CDN URL — those links can expire, and a finished deliverable shouldn't depend on a third party's link staying alive.
  1. Get the hosted URL from the generation result.
  2. Download it to local disk into an `images/` subfolder next to the HTML, with a descriptive filename: `curl -sL -o "images/slide1-hook-<description>.png" "<generated image URL>"`.
  3. Reference the local relative path in the HTML, not the remote URL.
  4. If the download fails (commonly `403`/`blocked-by-allowlist`), this environment doesn't have the network access needed for that specific external host — say so directly rather than silently leaving a remote link in a "finished" file. Offer the hosted URL as a flagged temporary fallback, and note that since the destination is often a synced Dropbox folder, the user can drop images in themselves and you can rewire the HTML to local paths afterward.
  5. Never claim a download succeeded before confirming the file exists on disk.
- **Export viewport: set it to the real target resolution with `device_scale_factor=1`.** Do NOT use the old preview-size-plus-scale-factor trick (e.g. a 420px viewport with `device_scale_factor = 1080/420`). That approach caused a real, hard-to-diagnose failure on 2026-07-24: it only works if the `.slide` CSS width, the `carousel-track` translateX step, and the viewport width all agree on the *same* scaled-down number. In practice the HTML keeps `.slide` at the full canvas width (1080px) while the translate step assumes the preview width (420px), the two drift apart, and every slide past the first two or three exports blank or overlapping. Setting the viewport to the real resolution removes the entire class of bug — there's only one width in play, so nothing can disagree.
- **Match the translateX step to the real slide width.** The carousel track must step by the same number the slides are actually laid out at. If slides are 1080px wide, step by 1080 — never a hardcoded preview number.
- Export process follows the same Playwright pattern regardless of asset type — only the canvas dimensions, page/slide count, and CSS selectors change:

```python
import asyncio, os
from pathlib import Path
from playwright.async_api import async_playwright

INPUT_HTML = Path("asset.html")   # relative to this run's working directory — never hardcode an absolute path
OUTPUT_DIR = Path("export")       # ditto
OUTPUT_DIR.mkdir(exist_ok=True)

# Real target resolution — the SAME numbers the HTML lays slides out at. One width, no drift.
CANVAS_W = 1080
CANVAS_H = 1350         # 4:5 carousel; use the asset type's real canvas from Section 2
TOTAL_PAGES = 1         # 1 for a single graphic; N for a carousel or multi-page lead magnet

# Pre-installed browser if present, otherwise the pip-installed one (see the Chromium steps above)
PREINSTALLED = "/opt/pw-browsers/chromium"
launch_kwargs = {"executable_path": PREINSTALLED} if os.path.exists(PREINSTALLED) else {}

async def export_pages():
    async with async_playwright() as p:
        browser = await p.chromium.launch(**launch_kwargs)
        page = await browser.new_page(
            viewport={"width": CANVAS_W, "height": CANVAS_H},
            device_scale_factor=1,      # real resolution directly — do NOT scale a small preview up
        )
        html_content = INPUT_HTML.read_text(encoding="utf-8")
        await page.set_content(html_content, wait_until="networkidle")
        await page.wait_for_timeout(3000)  # let webfonts settle

        # hide any preview-only chrome (nav dots, frame borders, captions) before capture
        await page.evaluate("""() => {
            document.querySelectorAll('.preview-chrome').forEach(el => el.style.display='none');
        }""")
        await page.wait_for_timeout(500)

        for i in range(TOTAL_PAGES):
            if TOTAL_PAGES > 1:
                # Step by the REAL slide width, passed in — never a hardcoded preview number.
                await page.evaluate("""([idx, slideW]) => {
                    const track = document.querySelector('.carousel-track');
                    if (track) { track.style.transition = 'none'; track.style.transform = 'translateX(' + (-idx * slideW) + 'px)'; }
                }""", [i, CANVAS_W])
                await page.wait_for_timeout(400)
            await page.screenshot(
                path=str(OUTPUT_DIR / f"page_{i+1}.png"),
                clip={"x": 0, "y": 0, "width": CANVAS_W, "height": CANVAS_H}
            )
            print(f"Exported page {i+1}/{TOTAL_PAGES}")

        await browser.close()

asyncio.run(export_pages())
```

**Common export mistakes to avoid:**

| Mistake | Fix |
|---|---|
| Assuming Chromium is (or isn't) pre-installed | Check `/opt/pw-browsers/chromium` first; if missing, `pip install playwright` + `playwright install chromium` (no `--with-deps`) before giving up |
| Using a small viewport with `device_scale_factor` scaling | **Root cause of the 2026-07-24 blank-slide bug.** Set the viewport to the real canvas size with `device_scale_factor=1` |
| Hardcoding the carousel translateX step (e.g. `-idx * 420`) | Step by the real slide width, passed in as a variable — it must match the `.slide` CSS width exactly |
| Giving up on a missing `lib*.so` error | Extract it unprivileged via `apt-get download` + `dpkg-deb -x` and prepend to `LD_LIBRARY_PATH` |
| Using shell scripts to generate the HTML | Use Python `Path.write_text()` |
| Not waiting for fonts to load | Wait ~3000ms after `set_content` |
| Exporting preview-only chrome (nav dots, frame borders) | Hide it before screenshotting |
| Linking to a generator's CDN URL instead of downloading | See the sourcing/downloading steps above |

---

## 5. Graphic JSON template

```json
{
  "asset_type": "<single_social_graphic | carousel_slide | blog_header | lead_magnet_page | ad_creative | newsletter_header>",
  "page_or_slide": 1,
  "canvas": {
    "width_px": 0,
    "height_px": 0,
    "aspect_ratio": "",
    "platform": []
  },
  "brand": {
    "business": "<business slug — do not leave blank>",
    "style": "<from Business/[slug]/context/brand-voice.md + brand-board.md>",
    "logo_required": true,
    "logo_placement": "<from Business/[slug]/context/brand-board.md>",
    "brand_treatment": "<from Business/[slug]/context/brand-board.md>"
  },
  "copy": {
    "headline": "",
    "body": "",
    "cta": ""
  },
  "visual": {
    "scene_description": "",
    "subject": "",
    "setting": "",
    "mood": "",
    "lighting": "",
    "photorealistic_image_required": true,
    "color_palette": ["<hex values from Business/[slug]/context/brand-board.md>"]
  },
  "layout": {
    "composition": "",
    "text_placement": "",
    "headline_hierarchy": "",
    "negative_space": "",
    "page_or_slide_counter": ""
  },
  "typography": {
    "headline_style": "<from Business/[slug]/context/brand-board.md>",
    "body_style": "<from Business/[slug]/context/brand-board.md>",
    "font_direction": "<from Business/[slug]/context/brand-board.md>"
  },
  "export": {
    "file_format": "PNG",
    "dimensions": "<matches canvas.width_px x canvas.height_px>",
    "safe_margins": "Keep all text and logo inside the business's documented safe margin, or 80-110px if none is documented",
    "quality": "High resolution, platform-ready"
  }
}
```

Rules:
- Never fill `brand`, `color_palette`, or typography fields with invented values — pull them from `Business/[slug]/context/brand-board.md`, or leave a clear placeholder noting the context is missing.
- `canvas` dimensions come from Section 2's table unless `brand-board.md` overrides them.
- Valid JSON only — double quotes, no trailing commas, no comments inside the JSON block.
- If an image will be AI-generated rather than a real photo, say so plainly to the user.

---

## 6. Quality bar

- Every color, font, and layout instruction traces back to `Business/[slug]/context/brand-board.md` — nothing invented.
- Canvas dimensions match the asset type's actual destination (a blog header isn't sized like a carousel slide).
- Visual direction is specific (mood, layout, image type), not generic "professional photo" filler.
- If images are AI-generated, that's disclosed.
- If `brand-board.md` or `style-guides/visuals.md` was incomplete, that's noted rather than papered over.
- Exported files (Mode F) are confirmed on disk before being presented as finished, and any download/rendering failure is stated plainly rather than silently worked around.

---

## 7. Save Your Output

`Business/[slug]/visuals/` is this skill's primary output destination — it's the one skill in this project that actually renders visual assets, and every other content skill hands off to it rather than producing its own visuals. Keep that handoff pattern intact: this skill is the only one that writes into a business's `visuals/` folder.

The `visuals/` folder already exists once the profile has been set up (e.g. `Business/[slug]/visuals/`) — don't create new folders, just save files into the existing one for the business identified in Section 1.

**Save automatically, every time, as part of producing the output — don't ask "should I save this?" first.**

Filename pattern for everything saved here: `YYYY-MM-DD_[asset-type]_[short-descriptive-slug].[ext]` — date is today's date, asset-type identifies what was produced, and the slug is a short human-readable description.

- **Mode D (design brief):** save the brief as a `.md` file, asset-type `design-brief` — e.g. `2026-07-09_design-brief_fall-promo-carousel.md`.
- **Mode E (JSON prompts):** save each JSON prompt as its own `.json` file, asset-type matching the asset being produced — e.g. `social-graphic`, `blog-header`, `lead-magnet-page-1`, `ad-creative`, `newsletter-header`, or `carousel-slide-1-of-5` for one slide in a set. For a multi-asset output (a 5-slide carousel, a multi-page lead magnet), save one file per slide/page, numbered in the filename — e.g. `2026-07-09_carousel-slide-1-of-5_fall-promo.json`, `2026-07-09_carousel-slide-2-of-5_fall-promo.json`, and so on.
- **Mode F (HTML/PNG export):** save the exported `.png` file(s) using the same naming pattern and slide/page numbering, one file per slide/page — this should succeed in most sessions (see Section 4's Chromium steps, which cover both the pre-installed and install-it-yourself cases). If Chromium genuinely can't be obtained in a given session (all three steps checked and failed, not assumed), don't let the run produce nothing — save whatever intermediate artifact does exist instead, such as the HTML file or the Mode E JSON prompt, so `Business/[slug]/visuals/` still ends up with something usable from that run. **Before declaring a multi-slide export finished, open or check at least one slide past the second** — the classic failure mode here renders slides 1-2 correctly and everything after them blank, so a spot-check of only the first slide will pass a broken run.

**Delivering the rendered file.** Writing it into the workspace *is* the delivery, not a step before it.

1. **Write it to `Business/[slug]/visuals/`** using the filename pattern above, and write the re-renderable source (the Mode E spec JSON, or the HTML) beside it with the same filename stem. State the full path in your reply. That file is what the business keeps; the conversation is not storage.
2. **Confirm the write before you report it.** List the folder or check the file exists. Never report a `visuals/…png` path you did not verify — a fabricated save confirmation is worse than an honest failure.
3. **Showing the image in the conversation is a surface-dependent extra.** If this surface can display or attach the file, do it *after* the file is written, and still give the path in the same turn. If it can't, say nothing about it — the saved file is already the deliverable. Do not call a tool to hand the file over unless you have confirmed that tool exists in this session; assume none does.
4. **In `storage_mode: dropbox`, binaries do not go through the connector** — `create_file` is text-only. Write the spec JSON or HTML through the connector so the image can be re-rendered, keep the rendered file in the local working folder, and say plainly that the image itself did not sync and where the source landed. Never list a Dropbox `visuals/…png` path the connector could not write.

Check the `visuals/` folder before saving (per Section 1, step 4) so filenames, numbering, and canvas dimensions stay consistent with what's already there — don't reuse a slide number or asset name that's already taken.

---

## 8. Response behavior

**If the business isn't clear:** ask before designing anything — see Section 1, step 0.

**If handed off from another skill with copy already approved:** design directly from that copy — don't ask the user to re-describe what they already specified in the content skill.

**If asked directly (no prior skill handoff) with just a topic:** ask what the copy/content actually is first, or offer to invoke the matching content skill (per the table in Section 2) to produce it — this skill designs from finished copy, it doesn't originate messaging on its own.

**Before attempting Mode F:** verify `/opt/pw-browsers/chromium` exists in the current session (a quick `ls`, not an assumption) — it did on 2026-07-10 but did NOT on 2026-07-24, so this genuinely varies. If it's missing, don't announce failure yet: work the install/`LD_LIBRARY_PATH` steps in Section 4 first (they took under a minute on 2026-07-24). Only offer Mode D or Mode E as a fallback if those steps also fail, and say which one failed.

**Every response that produces output:** confirm what was saved to `Business/[slug]/visuals/` and list the file path(s) for every asset produced in that run — don't just describe what was made, show where it landed. If a file could not be written where it should have been (Section 7), say so plainly rather than listing a path that doesn't exist.

---
name: business-setup
description: >
  Builds the business profile every other skill reads: starts from the customer's website (real copy, colours, fonts, and logo where a scrape tool is available), adds a short plain-English interview to confirm what was found and capture what no website shows, then writes the full Business/[slug]/ folder — context/ with brand-voice, audience, products, brand-board and seven style guides, plus seo/, social/, visuals/ and examples/. Works with no website and no connectors: the interview alone produces the same files. On a first run it also initializes memory.md and aimm-config.md, and it finishes by running doctor. Use when the user wants to set up or update their business profile, is installing for the first time, or asks any skill to produce something before a profile exists.
---

# Business Setup

Every skill in this plugin is only as good as the `Business/[slug]/context/` folder it reads. This skill's entire job is building that folder — fast, and grounded in whatever real material exists, rather than generic placeholder content dressed up to look finished.

This skill produces a *complete, real* context folder or it says plainly what's still missing. It does not produce a folder that looks complete but is actually padded with invented brand details — that's worse than an honest placeholder, because every downstream skill will trust it silently.

---

## Workspace and file access — resolve this before any read or write

Every `Business/...`, `memory.md`, and other workspace path in this skill is relative to your workspace root. Resolve it **once** at the start of the run, then use the same method for every read and write that follows:

1. **The current project folder is the workspace root.** If a folder is open or mounted in this session, that folder is the root. This is the default and needs no configuration.
2. **`aimm-config.md` at that root can override it.** If it sets `workspace_root`, use that path instead. If it sets `storage_mode: dropbox`, read and write through the Dropbox MCP tools (`list_folder`, `fetch`, `create_file`, `delete`) at that path. Dropbox is used only when the config says so, and only at the path the config gives — never a built-in one.
3. **Nothing reachable.** Say so in one line and ask which folder to use, then work from what you're told in chat. Never invent a workspace path or brand context, and never quietly produce generic content as if context had been read.

A failed read is **not** proof a file is missing. Retry, or list the parent folder, before reporting anything absent — especially before saying a business profile doesn't exist.

**Finding a connector:** where a later section needs one, find it by **capability, not by name** — connector prefixes differ between installs, so never match a literal `mcp__…` string and never conclude a connector is absent because one guessed name failed. In the default local mode no connector is involved at all: write to the workspace folder directly.

**Before falling back to a lesser path,** check `.aimm/environment.md` for what `doctor` last found. Treat it as a hint, not proof — if it is stale or absent, probe and proceed. The live probe is always authoritative.

**Plugin-relative paths are the exception.** Paths beginning `assets/`, `scripts/`, `library/`, or `references/` live inside this skill's own folder in the installed plugin — *not* in the workspace root and *not* in Dropbox. Read those from the skill directory on every surface, mobile included, and never look for them through a connector.

**Writing in Dropbox mode:** Dropbox cannot append or edit in place. Fetch the file's live content immediately before changing it, then delete and recreate it at the same path. Never write from an earlier read.

**One business per workspace.** The active slug comes from `aimm-config.md` (`business:`), or the single folder under `Business/` that isn't `_template`. If several exist and the config is silent, ask once. Never mix two businesses' content.

---

## 0. First run in this workspace? Initialize it first

Before setting up the business itself, check whether this is the very first time AI Marketing Machine has run in this workspace. Look for `memory.md` at the workspace root as resolved above. Don't ask which folder the workspace is in — the resolution order already answers that. Only ask if nothing is reachable at all.

**If it doesn't exist yet (first-ever setup),** create the three items below, copying the context scaffold from `Business/_template/`.

**The signal for "first run" is a missing business profile under `Business/`, not a missing `memory.md`.** The menu, `doctor`, and this skill all use that one signal so they cannot disagree — a workspace with a `memory.md` but no profile is still a first run.

1. **`memory.md` at the workspace root** — the running log, read at the start of every session. Initialize with empty `## Active work`, `## Recent decisions`, and `## Open threads` sections plus a one-line header explaining it should be updated as decisions get made, not batched later. Start it genuinely empty; never seed it with another install's history.

2. **`aimm-config.md` at the workspace root** — the settings file. Write it with `business:` set to the slug being created now and every other key left blank, so the defaults apply. Copy `Business/_template/aimm-config.example.md` as the starting point — it documents every key and its default inline. If the file already exists, update `business:` rather than rewriting the file.

3. **`Business/_template/`** — the setup scaffold. If it already exists, use it as-is; do not recreate or duplicate it. If it doesn't, create `Business/_template/context/` with `brand-voice.md`, `audience.md`, `products.md`, `brand-board.md`, and a `style-guides/` subfolder containing `social.md`, `blog.md`, `ads.md`, `email-newsletter.md`, `landing-pages.md`, `lead-magnets.md`, and `visuals.md` — each a clearly-labeled placeholder stating what belongs in it, plus `CLAUDE.md` and `memory.md` for the per-business context layer. Placeholders must read as obviously unfilled, never as invented brand facts.

**If they already exist,** this is a re-run or an update — skip straight to Section 1 and do not overwrite the root `memory.md` or `aimm-config.md`.

In the default local mode, create folders and write files directly. In `storage_mode: dropbox`, create each parent folder before writing into it — the connector does not auto-create them.

---

## 1. Ask one question

> **"What's your website?"**

That is the whole opening. If they have a site, everything else can be inferred and then confirmed — which is faster and more accurate than an interrogation. If they say they don't have one, that's fine and common: go straight to Section 2c.

**Never ask for a "slug".** Derive it silently from the business name: lower-case, spaces to hyphens, drop punctuation — *Main Street Builders* → `main-street-builders`. It is an internal folder name. Words like "slug" and "kebab-case" mean nothing to a business owner and asking is the fastest way to make a product feel like a developer tool.

Only ask for the business name separately if the site doesn't make it obvious.

---

## 2. Research — gather real material before asking anyone to invent any

### 2a. Read the website

**Do all three of these, not just the first.** Capturing colours but not copy is what produces a beautiful `brand-board.md` next to a thin `audience.md`.

1. **Visual identity.** If a Firecrawl scrape tool resolves in this session (find it by capability, per the section above — check before assuming either way), scrape the homepage with `formats: ["branding", "screenshot"]`. This returns real hex colours by role, font families, button styling, logo URL, favicon and og:image, pulled from the site's rendered CSS rather than guessed.
2. **Copy, positioning, and offers.** Scrape with `formats: ["markdown"]` on the homepage **and the 2–4 most content-bearing pages** — about, services, pricing, testimonials if linked. This is what actually fills `audience.md`, `products.md`, and most of `brand-voice.md`. Site copy is load-bearing evidence: the words already chosen for a live site show the real voice.
3. **Third-party signal.** One or two targeted searches — "[business name] reviews", "[owner name] interview" — often surface proof points and a plainer voice than the site itself.

**If no Firecrawl tool resolves,** use `WebFetch` for the copy and leave `brand-board.md` explicitly unfilled, noting *why* (no visual-capture tool this session) so a later run knows to backfill. **Never invent hex codes to compensate.**

Two honesty rules on anything captured:

1. **Label the source.** "Source: captured from live site CSS, [date]." This is the palette the audience actually sees — real enough to design against, but not the same as a business-confirmed brand system.
2. **Flag templated platforms.** Squarespace, Wix, and industry-specific platforms usually give themselves away in CDN hostnames. A template's palette may be a theme default rather than a deliberate choice. Keep the values, add one line flagging it, and recommend confirming before it anchors bigger design work.

### 2b. Read anything else they have

If they mention social accounts, existing documents, or a cloud folder, use it — real published captions are better evidence of voice than site copy, which is often written once by a web vendor.

- **Pasted captions** (best): read directly for tone, rhythm, emoji and hashtag habits, CTA patterns.
- **Public post URLs**: try a scrape, but Instagram and Facebook aggressively login-wall content — expect failures and don't burn the pass retrying.
- **Just a handle**: ask them to paste 3–5 posts they think are representative. Thirty seconds of copy-paste beats an unreliable scrape, and *which* posts they pick is itself signal.
- **A cloud folder**: search and read anything that looks like deliberate brand material — a brand guide, a positioning doc, a pricing sheet.

A couple of posts is a thin sample. Say so in `brand-voice.md` rather than presenting patterns inferred from two captions as settled rules.

### 2c. The interview — always, not only when there's no website

**A scrape gets the facts roughly right and the personality entirely wrong.** These questions fill what no website exposes, and let the owner correct what was captured. Run them every time.

Ask **one at a time**. Wait for the answer before the next. Dumping six questions in one message is the fastest way to lose someone on their first run.

1. What's your business — what do you sell?
2. Who's your customer? Describe one real person who buys from you.
3. What's the one thing you want someone to do after seeing your stuff — call, book, buy, message you?
4. Tell me one thing that happened in your business recently — a job, a win, a problem you sorted out.
5. What's your vibe — plainspoken, professional, warm, funny, no-nonsense?
6. What's one thing you believe about your industry that a lot of people in it would disagree with?

**After question 1, load the matching starter pack.** Q1's answer is the trade, and `references/starter-packs/` holds six: `home-and-trades`, `food-and-hospitality`, `professional-services`, `health-and-wellness`, `retail-and-ecommerce`, `property`. Read the one that fits and use it two ways:

- **Sharpen the remaining questions.** "Most trades businesses find people can't tell why two quotes differ — is that what you hear?" is a better question than "who's your customer?", and it is answerable.
- **Seed the write step in Section 3**, so the profile starts from trade-typical content rather than blank.

**The pack is a starting point, never a finding.** Every line it seeds carries `[starter-pack default]` and stays that way until the owner confirms it. Strip the marker on the ones they confirm or correct; leave it on the rest. If none of the six fits, say so and carry on without one — a wrong pack is worse than none.

**Question 6 is the wedge**, and it is the highest-leverage answer in the whole run — content with a point of view travels, content that agrees with everyone gets scrolled past. It is also the one people freeze on. If they draw a blank, offer to skip it and come back later, and write "Not yet captured" rather than leaving it blank, so later skills know to ask rather than assuming there's no opinion.

**When a website was scraped, shorten this.** Lead with what you found and ask them to correct it — "Your site says you mostly do kitchen work for period properties. Is that still right, or has it moved on?" Confirming is faster than asking cold, and it catches a stale site, which is common.

**Then ask what the site can never tell you** — questions 4, 5, and 6 at minimum. A business with a website still needs these; without them the profile has facts and no personality.

Don't pad thin answers into something that sounds more finished than it is. A short, honest `audience.md` beats a long, invented one.

---

## 3. Build the folder

Every business gets the same shape — one folder, five subfolders, no exceptions and no structural variants. `Business/[slug]/`:

- `context/` — the brand facts every skill reads before producing anything. Mirrors `Business/_template/context/` exactly.
- `seo/`, `social/`, `visuals/`, `examples/` — empty output folders, created now so every content skill finds them on its first run rather than needing to create them ad hoc mid-task.

1. Create `Business/[slug]/context/` and `Business/[slug]/context/style-guides/`, mirroring `Business/_template/context/`'s structure exactly — that scaffold is the full shape. In `storage_mode: dropbox`, create each parent folder first; the connector does not auto-create them.
2. Write each context file using real material gathered in Section 2, plus the starter pack where it applies. **Confirmed answers always beat pack defaults** — where the owner said something, use their words and drop the marker. Where they didn't, keep the pack line *and* its `[starter-pack default]` marker so the gap is visible rather than hidden:
   - `brand-voice.md` — positioning, voice pillars, tone, vocabulary use/avoid, messaging framework, CTA toolkit, do's/don'ts. Follow the structure in `Business/_template/context/brand-voice.md`. **Write interview answers 5 and 6 into `## Tone` and `## Strong opinion / wedge`, and answer 4 into `## Recent stories worth telling`.** The wedge is the highest-leverage line in the whole profile — if it wasn't captured, write "Not yet captured" rather than leaving it blank.
   - `audience.md` — who content is for, segments/tiers if any exist, pain points/desires/decision triggers, archetypes, where they actually spend time.
   - `products.md` — offerings, pricing (flagged as tested or provisional), the actual funnel/next-step, and an explicit honesty-flags section if the business is pre-revenue/pre-case-study or otherwise can't back up proof-style claims yet.
   - `brand-board.md` — logo rules, color palette (hex values only if real ones exist — never invent brand colors), typography, photography direction, layout patterns if any exist. If no visual identity exists yet, say so explicitly rather than filling this in with generic "clean and modern" filler.
   - **All seven `style-guides/`** — each carries real headings; fill every one you have evidence for and leave the rest as the bracketed hint. `social.md` matters most (which platforms this business actually uses, cadence, content pillars, hashtag and CTA conventions) and is worth the most effort. `ads.md` leads with "Is paid an active channel?" — **answer that one explicitly even if the answer is no**, because campaign skills check it before proposing a budget, and an unanswered question reads as yes. Don't guess at tactics the research didn't support; an honest bracketed hint is better than an invented convention.
3. Every file should carry a one-line **source note** at the top — "Source: [document/URL/interview date]" — so anyone reading the file later knows whether it's real material, an inference, or a placeholder.
4. If the business supplied raw assets during research (logo files, brand kit documents, sample graphics, rights-cleared photography) that aren't themselves brand *facts* to transcribe into `context/`, keep them referenced by source (URL, or where they live in the business's own Dropbox) rather than duplicating large binary files into this project — `context/brand-board.md` should point to where the real logo file lives, not try to store a copy.
5. Create the four output folders — `Business/[slug]/seo/`, `social/`, `visuals/`, `examples/`. Then copy `Business/_template/social/content-calendar.md` into `Business/[slug]/social/`, replacing `[Business Name]` with the real business name. Copy it rather than retyping it — the template carries the Performance and Verdict columns and the benchmarks block that `performance-digest` writes into.
6. Create `Business/[slug]/CLAUDE.md` and `Business/[slug]/memory.md` from `Business/_template/CLAUDE.md` and `Business/_template/memory.md`, filling in the real business name and what's known so far. This is what gives the business their own context-inheritance layer — Claude Code reads this automatically whenever work happens inside your business's folder, on top of the root `CLAUDE.md`/`memory.md`.

---

## 4. Wire it in

1. Set `business:` in `aimm-config.md` at the workspace root to this slug, so every skill resolves it without asking.
2. Fill in `Business/[slug]/memory.md`'s **Status**, **Active work**, and **Honesty flags** sections — mirroring anything flagged in `products.md` so skills that don't read that file still see it. This is the business's own memory file, not the root one.
3. Confirm all five folders (`context/` fully populated, `seo/`, `social/` with its seeded `content-calendar.md`, `visuals/`, `examples/`) exist per Section 3 — this is part of "wired in," not optional polish, since content skills will look for these folders on their very first run.
4. **Run `doctor`.** It writes `.aimm/environment.md` and gives the user their first honest picture of what this installation can and can't do. Setup is where that belongs — it is the moment they most need to know whether publishing is connected.

---

## 5. Validate before treating this as done

Setup isn't finished when the files exist — it's finished when a skill can actually produce good output from them. Do both checks.

**The mechanical check** — run it first, it's cheap and catches the common failure:

1. All four `context/` files and all seven `style-guides/` files exist.
2. **None of them still says `Status: not yet filled in`** unless you can name why that one had no evidence behind it.
2b. **Count what is still `[starter-pack default]`.** A pack line the owner never confirmed is not the same as a filled file — it is trade-typical text standing in for them. This is the check that stops a pack turning "11 of 11" into a lie.
3. `social/content-calendar.md` exists and carries the Performance and Verdict columns.
4. `aimm-config.md` has `business:` set to the slug.
5. Report the count plainly, and **split confirmed from seeded**: "11 of 11 filled — 7 from what you told me, 4 still starter-pack defaults for your trade that we haven't confirmed yet." Or "9 of 11 — `blog.md` and `email-newsletter.md` are still empty because we didn't cover blogging or email." A gap you can name is fine. A gap you can't is a hole in Section 2. **Never report a pack default as filled without saying so** — that is the one way this step can mislead.

**The judgement check:**

6. Produce one real piece of content against the new profile — `social-creative-designer` is the fastest.
7. Show it and ask directly: does this sound like you, or does it read generic? A profile that produces generic output has a gap somewhere in Sections 2–3 even when every file is technically filled.
8. If it fails, don't patch the one output — find which context file was thin and fix it there, so every skill benefits.
9. Write the result into `Business/[slug]/memory.md`'s **Validation status**: what was produced, and whether the user recognised their own voice in it. That is the evidence a future session needs, and it is currently the thing most often discarded.

---

## 6. Quality bar

- Nothing in `brand-voice.md` or `brand-board.md` is invented — every color, tone word, or messaging pattern traces back to real material or an explicit interview answer.
- Placeholders are honest: a file that's genuinely unfilled says so, using the same "Status: not yet filled in" convention, rather than being padded to look complete.
- `products.md` carries an explicit honesty flag if the business can't yet back up proof-style claims (no testimonials/results yet) — this is the single most important flag to get right, since it constrains every content skill downstream.
- The slug was derived silently and used consistently — the folder name and the name skills are told must not drift apart.
- The validation step (Section 5) actually happened — **both** checks — not just the file-writing step.
- The customer was never asked for a "slug", "kebab-case", or any other word from inside the software.
- The interview ran even when a website was scraped. A profile with facts and no personality is a half-finished profile.
- Every starter-pack line the owner didn't confirm still carries its `[starter-pack default]` marker. Stripping markers to make the count look better is the failure this whole mechanism exists to prevent.
- The pack never wrote hex codes, target keywords, offerings, pricing, or a recent story.
- `doctor` ran at the end, so the user leaves knowing what this installation can and can't do.

---

## 7. Response behavior

**If the user gives a business name with no other detail:** ask what source material exists (Section 1, step 2) before doing anything — don't start interviewing or researching blind.

**If research surfaces conflicting information** (e.g., a website says one price, a pricing doc says another): flag the conflict to the user rather than picking one silently.

**If asked to onboard multiple businesses in one request:** do them one at a time, fully, rather than shallowly filling in several folders at once — a half-built context folder is worse than not having started, because it looks done to every skill that reads it.

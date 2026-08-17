---
name: seo-audit
description: >
  Runs a comprehensive SEO audit — technical SEO, on-page checks, keyword research, content gaps, competitor comparison, plus a dedicated Local SEO / Google Business Profile / AI-citation-readiness audit (NAP consistency, review velocity, the ~150-review AI-citation threshold, local pack factors). Reads brand voice, audience, and service area from Business/[slug]/context/ at runtime rather than hardcoding any brand, and checks Business/[slug]/seo/ first so it never duplicates existing research. Use for an SEO audit, site audit, keyword research, content gap analysis, technical SEO check, competitor SEO comparison, Google Business Profile review, local SEO check, or "why aren't we ranking" / "why isn't this business showing up in AI search." Produces a prioritized action plan, not just a diagnosis.
---

# SEO Audit

Audits a business's SEO health — technical, on-page, keyword, competitive, AND local/Google Business Profile — and produces a prioritized action plan a non-technical business owner can act on. This is the diagnostic and strategy layer; `ai-search-blog-writer` writes the content this audit recommends, and `campaign-plan` can sequence the fixes into a calendar.

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

## 0. Read the business context

The active business is already resolved. Before doing anything else:

1. **Confirm the business profile.** The active business was resolved once at the top of this skill — don't re-resolve or re-ask here. If no profile exists yet, stop and run `business-setup` rather than writing against an empty context folder.
2. Read `memory.md` at the project root for active projects and open threads.
3. Read `Business/[slug]/context/brand-voice.md`, `audience.md`, `products.md` — especially the **Service area / market** field in `products.md`, since local SEO work is meaningless without knowing the geography being targeted.
4. Read `Business/[slug]/context/brand-board.md` for the business's actual website URL and any listed profiles (this is usually where a captured URL lives from onboarding).
5. Check `Business/[slug]/seo/` for prior audits, keyword research, or content briefs. **Don't re-run research that already exists** — read what's there, note what's changed since, and build on it rather than duplicating it. This matters most for keyword research, since `ai-search-blog-writer` already saves content briefs here.
6. Check `Business/[slug]/social/content-calendar.md` and `Business/[slug]/examples/` for what's actually been published, so gap analysis is grounded in reality, not guesswork.

**If the business has no confirmed website URL,** ask for it before proceeding — this skill cannot audit a site it can't reach.

**If any context file is an unfilled placeholder,** say so, then proceed on available information and general best practice rather than blocking.

---

## 1. Inputs

Gather the following. If not provided, ask before proceeding:

1. **URL or domain** — the site to audit (from `brand-board.md`/`products.md` if already known, otherwise ask).
2. **Audit type** — one of:
   - **Full audit** (default) — everything below.
   - **Local SEO / Google Business Profile audit** — Section 4 only.
   - **Keyword research** — Section 2 only.
   - **Content gap analysis** — Section 5 only.
   - **Technical SEO check** — Section 6 only.
   - **Competitor comparison** — Section 7 only.
3. **Target keywords** (optional) — terms the business already targets or wants to rank for.
4. **Competitors** (optional) — if not given and the audit type needs them, identify 2-3 likely competitors via web search based on the business's service area and offerings from `products.md`.

---

## 2. Keyword Research

**Disclosure first:** no SEO data connector (Ahrefs, SimilarWeb, SE Ranking, DataForSEO) is authorized in this environment as of this writing. Check anyway — if a connector like this is connected when you run, use it and report real search volume, keyword difficulty, and ranking data. If not, say explicitly: *"No SEO data tool is connected — the estimates below are directional, from search-pattern research, not measured volume or difficulty. Connect Ahrefs, SimilarWeb, or SE Ranking via MCP for real numbers."* Never present an estimate as if it were measured data.

For each keyword opportunity, assess:
- **Primary keywords** — high-intent terms tied directly to what's in `products.md`.
- **Local-intent keywords** — "[service] in [city/neighborhood]," "[service] near me," and named-neighborhood variants pulled from the business's actual service area, not generic city-level terms only. For real estate, builder, and local-service businesses, this category usually matters more than broad national terms.
- **Secondary and long-tail keywords** — supporting terms and specific lower-competition phrases.
- **Question-based keywords** — phrased the way someone would ask an AI assistant, not just type into a search bar (mirrors `ai-search-blog-writer`'s GEO guidance — reuse its conversational-phrasing logic rather than re-deriving it).
- **Intent classification** — informational, navigational, commercial, transactional, or local-commercial.
- **Search demand and difficulty** — relative (high/medium/low) unless real data is available.

Cross-reference against `Business/[slug]/seo/` (step 0.5) so this list adds to existing research instead of repeating it.

---

## 3. On-Page SEO Audit

For the homepage, top service/listing pages, and recent blog posts, evaluate:

- **Title tags** — present, unique, 50-60 characters, includes the target keyword.
- **Meta descriptions** — present, compelling, under 160 characters, includes a CTA.
- **H1/H2/H3 structure** — one H1 per page, logical hierarchy, secondary keywords used naturally.
- **Keyword usage** — primary keyword in the first 100 words, natural throughout, never stuffed.
- **Internal linking** — related pages link to each other; flag orphan pages.
- **Image alt text** — descriptive, keyword-included where genuinely relevant.
- **URL structure** — clean, readable, includes keywords.

Use Firecrawl if available (this project already relies on it for brand/visual capture — see `business-setup`) to pull raw HTML, meta tags, and JSON-LD that a plain fetch won't surface. If Firecrawl isn't available, use `WebFetch`/`WebSearch` and note the reduced fidelity (structured data and JS-rendered content may be invisible to a plain fetch).

---

## 4. Local SEO & Google Business Profile Audit

**This is the section most likely to move the needle for a local business** — trades, builders, remodelers, and small local businesses live or die by local pack visibility, not broad national rankings. Current research (2026) puts Google Business Profile signals at roughly a third of local ranking weight, ahead of on-page, review, link, and citation signals individually — and AI Overviews / ChatGPT / Perplexity rarely name a local business as a recommendation below roughly 150 reviews per location. Audit accordingly, even when the business didn't explicitly ask for "local SEO."

There is no Google Business Profile API connector in this environment — everything here is via `WebSearch`/`WebFetch` against what's publicly visible (the Google Maps/Search listing, review platforms, directory sites). Say so plainly in the output; don't present observed signals as if pulled from the GBP API.

Check and report on:

- **Listing completeness** — business name, category, hours, service area, description, and photos as they appear in public search results.
- **Review volume vs. the AI-citation threshold** — current review count against the ~150-review benchmark. If well under, name this explicitly as a priority: it's not just a vanity metric, it's a gate on whether AI assistants will recommend the business at all.
- **Review velocity** — recent review cadence (are reviews arriving steadily, or is the profile stale?). A competitor gaining reviews monthly will out-rank a business sitting on old ones — check competitor review counts and recency for contrast.
- **Review response rate** — whether the business appears to reply to reviews (visible in the public listing). Response rate is a measurable signal, not just good customer service.
- **NAP consistency** — Name, Address, Phone number matching exactly across the business's own site, Google, Facebook, and any other directories it's found on. Flag every mismatch found — these actively suppress local ranking.
- **Local schema markup** — whether the site uses `LocalBusiness` (or a more specific subtype) structured data; flag if missing.
- **Local-intent on-page signals** — service-area pages, city/neighborhood-specific content, embedded map, local keyword usage per Section 2.
- **Map-pack competitive position** — for the business's top 2-3 target local searches, note who currently holds the map pack and what's observably different about their listings (review count, photo volume, category selection).

---

## 5. Content Gap Analysis

Identify what's missing from the business's content strategy:

- **Competitor topic coverage** — topics/keywords competitors cover that the business doesn't.
- **Content freshness** — pages untouched for 12+ months that may be losing ground.
- **Thin content** — pages too shallow to rank for their intended query.
- **Missing formats** — guides, comparison pages, neighborhood/service-area pages, FAQs the business doesn't have but competitors or search demand suggest are needed.
- **Funnel gaps** — missing content at specific stages (awareness, consideration, decision) relative to what `products.md`'s funnel/CTA section describes.

For each gap, flag whether it's a fit for `ai-search-blog-writer` (blog/article), `landing-page-builder` (a dedicated page), or `lead-magnet` (a gated asset) — this audit should point at the right downstream skill, not just describe the gap.

---

## 6. Technical SEO Checklist

- **Page speed** — likely causes of slowness (large images, render-blocking scripts, excess redirects) based on observable page behavior.
- **Mobile-friendliness** — responsive layout, tap targets, viewport configuration.
- **Structured data** — schema opportunities beyond LocalBusiness: Article, FAQPage, Product, Review, BreadcrumbList.
- **Crawlability** — robots.txt, XML sitemap presence/accuracy, canonical tags, noindex/nofollow usage.
- **Broken links** — internal/external 404s, redirect chains.
- **HTTPS** — secure connection, mixed-content issues.
- **Core Web Vitals signals** — LCP/INP/CLS indicators from observable behavior (not lab data, unless a connector provides it).

---

## 7. Competitor SEO Comparison

For each competitor identified in Section 1 or found via search:

- **Keyword overlap and gaps** — shared terms, and terms only the competitor ranks for.
- **Local pack presence** — whether they appear in the map pack for the business's priority local searches, and what their listing has that the business's doesn't (see Section 4).
- **Content depth and publishing cadence** — relative content volume and freshness.
- **Domain authority signals** — directional, based on observable backlink/mention patterns, not a precise score unless a connector provides one.
- **SERP feature ownership** — who holds featured snippets, People Also Ask, local packs, or knowledge panels for shared target terms.

---

## 8. Output

### Executive Summary
3-5 sentences. Lead with whichever lever is actually highest-impact for your business — for most businesses in this project's vertical, that's Section 4 (local/GBP), not generic technical fixes. State the site's biggest strength, the top 3 priorities, and an overall health call: strong foundation, needs work, or critical issues.

### Local SEO / GBP Scorecard
| Signal | Status | Benchmark | Fix |
|---|---|---|---|
Include review count vs. the 150-review threshold, NAP consistency, listing completeness, response rate, and local schema presence at minimum.

### Keyword Opportunity Table
| Keyword | Intent | Est. Difficulty | Local vs. Broad | Recommended Content Type | Owning Skill |
|---|---|---|---|---|---|
15-25 opportunities, sorted by priority. "Owning Skill" points to `ai-search-blog-writer`, `landing-page-builder`, or `lead-magnet`.

### On-Page & Technical Issues
| Page/Area | Issue | Severity | Fix |
|---|---|---|---|
Severity: Critical (blocks indexing/ranking), High, Medium, Low.

### Content Gap Recommendations
Topic, why it matters, recommended format, priority, effort estimate, owning skill.

### Competitor Comparison Summary
| Dimension | This Business | Competitor A | Competitor B | Winner |
|---|---|---|---|---|
Include local pack presence as a row, not just generic keyword/content metrics.

### Prioritized Action Plan
**Quick wins (this week):** under ~2 hours each, immediate impact — e.g., claim/complete GBP fields, fix NAP mismatches, add missing meta descriptions, respond to outstanding reviews.
**Strategic investments (this quarter):** review-generation campaign, topic cluster build-out, service-area page rollout, structured data implementation.

Each action item: what to do, expected impact, effort estimate, dependencies, and which skill (if any) executes it.

---

## 9. Save your output

Save automatically once the audit is complete — don't ask first.

**Audit report** → `Business/[slug]/seo/YYYY-MM-DD_seo-audit_[site-or-topic-slug].md`
The full audit as structured above. Use today's actual date and a short readable slug.

If the audit surfaced clear next steps, say so explicitly and offer, don't auto-run: *"Want me to turn the top keyword opportunities into content briefs with `ai-search-blog-writer`, or sequence this into a plan with `campaign-plan`?"*

---

## 10. Quality bar

- Every claim about search volume, difficulty, or authority is labeled as measured (connector-sourced) or directional (search-pattern estimate) — never presented ambiguously.
- Local SEO/GBP section is included even when not explicitly requested, for any business whose `products.md` service area indicates a local/regional business — flagged as included-by-default with a one-line reason, not silently added.
- No fabricated review counts, ranking positions, or competitor data — everything is either observed via search/fetch or explicitly marked as an estimate.
- Recommendations point to the specific downstream skill that executes them, not just a description of what should happen.
- Matches `Business/[slug]/context/brand-voice.md` tone in the executive summary and recommendations (a technical audit still shouldn't read like it was written for a different client's voice).
- If `Business/[slug]/context/` was incomplete, that's noted rather than papered over.

## 11. Response behavior

**If the business isn't clear:** ask before starting — see Section 0.

**If given only a URL with no other input:** run a full audit and state the assumptions made (audit type, competitors chosen) at the top.

**If asked to re-run after a previous audit exists in `Business/[slug]/seo/`:** don't start from scratch — read the prior audit, note what's changed, and produce a delta-focused update rather than a full duplicate.

**After saving:** confirm the save with the actual file path, and surface the single highest-priority finding in the chat response even though the full detail lives in the file — don't make the user open the file to learn the one thing that matters most.

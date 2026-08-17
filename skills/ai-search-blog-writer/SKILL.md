---
name: ai-search-blog-writer
description: >
  Writes blog posts and articles optimized for both traditional SEO and AI-search visibility (being cited or summarized by ChatGPT, Perplexity, Google AI Overviews, and similar). Reads brand voice, audience, and products from your Business/[slug]/context/ folder at runtime rather than hardcoding any brand. Use whenever the user asks for a blog post, an article, SEO content, "something for the website," or content meant to rank or get cited when someone asks an AI assistant a question in this brand's space — even if they don't say "SEO" or "AI search" explicitly.
---

# AI-Search Blog Writer

You're writing for two readers at once: a human scanning the page, and an AI system that might read the whole thing once and then summarize or quote three sentences of it to someone who never visits the page at all. Both matter — as of 2026, a meaningful share of searches resolve without a click, and Google's own guidance confirms the fundamentals (unique, valuable, well-structured content) still drive both traditional rankings and AI-feature inclusion. GEO (generative-engine optimization) is additive to SEO, not a replacement for it — don't skip the SEO fundamentals to chase AI citations.

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
2. Read `Business/[slug]/context/brand-voice.md` — tone, vocabulary, what to avoid.
3. Read `Business/[slug]/context/audience.md` — who's reading, their pain points, and critically, **the exact language they use to describe their own problem** — this is what both search engines and AI assistants match against.
4. Read `Business/[slug]/context/products.md` — so the content stays grounded in what's actually offered, not generic industry advice.
5. Read `Business/[slug]/context/style-guides/blog.md` if it exists — any format/length/keyword conventions already decided.
6. Check `Business/[slug]/seo/` for existing keyword research and content briefs. Before proposing a new topic or keyword target, see what's already been covered for your business so you don't propose something redundant or cannibalizing an existing target.
7. Check `Business/[slug]/examples/` for prior finished blog posts, to calibrate voice and structure against what your business has actually published before. Both `Business/[slug]/seo/` and `Business/[slug]/examples/` may be empty for a business with no history yet — don't block on it, just proceed.

**If any of these are unfilled placeholders,** say so, then proceed on the brief and general best practice rather than blocking.

---

## 2. Structure

1. **Headline** — benefit-driven, includes the primary keyword, under ~60 characters for the SEO title tag (the on-page H1 can be slightly more natural-language if it reads better).
2. **Introduction (100-150 words)** — hook with a question, stat, or bold claim, then **answer the core question directly in the first 1-2 sentences** before elaborating. This "answer-first" structure is what both featured snippets and AI summarizers pull from — don't bury the actual answer three paragraphs down for the sake of a slow build.
3. **Body (3-5 sections, H2 each, H3 for subsections)** — one core idea per section, scannable, with a concrete supporting detail (a number, a named example, a specific process step) in every section. Generic sections that could belong to any competitor's article don't get cited — specificity is what AI systems quote.
4. **FAQ-style section (when the topic supports it)** — 3-5 direct questions in the audience's own words (from `Business/[slug]/context/audience.md`) with concise, complete-sentence answers. This block is easy for both people and AI systems to extract as a standalone answer, and maps cleanly to FAQ schema if the site supports it.
5. **Conclusion (75-100 words)** — summarize, reinforce the main claim, CTA.
6. **Meta description** — under 160 characters, includes the primary keyword, compels the click for the human readers who do click through.

---

## 3. Traditional SEO checklist

- Primary keyword in: headline, first paragraph, one H2, meta description, URL slug.
- 2-3 secondary keywords used naturally in body copy and subheadings — never keyword-stuffed.
- Title tag under ~60 characters; meta description under ~160.
- One H1 per page; logical H2/H3 hierarchy.
- Image alt text, descriptive, keyword-included where genuinely relevant.
- 2-3 internal links to related content; 1-2 external links to authoritative sources.
- Write for humans first — an AI system trained to detect keyword-stuffed, low-value content will not cite it either.

## 4. AI-search (GEO) specific practices

- **Answer-first structure** — see Section 2. State the direct answer before the explanation, in nearly every section, not just the intro.
- **Entity clarity** — be unambiguous about who/what is being discussed (brand name, service, location) rather than relying on pronouns and context the way a human reader would tolerate; AI systems extract passages out of context, so each passage should make sense on its own.
- **Information gain** — include something the audience can't get from the ten other articles on this topic: a specific number from real experience, a named local detail, a process step competitors don't explain. Generic, rehashed advice doesn't get selected as a citation when ten other pages say the same thing.
- **Conversational phrasing** — write some headers and FAQ questions the way someone would actually ask an AI assistant ("how much does X cost in [city]," "what's the difference between X and Y") rather than only keyword-string phrasing ("X cost [city]"). AI query patterns skew more natural-language than classic search-bar keyword strings.
- **Freshness** — date the content or reference current information where relevant; stale pages lose both rankings and AI-citation share over time. If updating an existing post, say so explicitly rather than silently changing it.
- **Consistent brand representation** — keep the brand's name, description, and key facts (location, services, positioning) consistent with how they appear elsewhere (site, `Business/[slug]/context/`, other content) — AI systems cross-reference entity information across sources, and inconsistency erodes citation confidence.

---

## 5. Output modes

### Mode A — Full draft
Default. Complete post per Section 2, ready to publish (pending human review).

### Mode B — Outline/brief only
When the user wants to review direction before a full draft: headline options, the core answer the post will lead with, the H2 section list with one line each on what it covers, and the target primary/secondary keywords. Stop there and wait for approval.

---

## 6. Quality bar

- The core question is answered in the first 1-2 sentences of the intro, not buried.
- Every section has at least one specific, non-generic detail.
- Tone matches `Business/[slug]/context/brand-voice.md`.
- Primary keyword and 2-3 secondary keywords are present and natural, not stuffed.
- FAQ section (if included) uses real audience phrasing from `Business/[slug]/context/audience.md`.
- No generic AI phrasing, no filler introductions ("In today's world...").
- If `Business/[slug]/context/` was incomplete, that's noted rather than papered over.
- Does not present unverified claims, results, or case studies as real — check `Business/[slug]/context/products.md` for any explicit honesty flags (e.g. a pre-revenue or pre-case-study business) before writing proof-style content.

---

## Save Your Output

Once the post is finished — and approved by the user if the request involved a revision loop — save two files automatically. Don't ask "should I save this?" first; save every time a post is completed.

1. **Keyword research / content brief** → `Business/[slug]/seo/YYYY-MM-DD_content-brief_[topic-slug].md`
   Capture the target keyword, search intent, related questions/topics considered (including anything ruled out because it was already covered per Section 1, step 6), and any competitive notes gathered while researching. This is the working research file, kept separate from the finished copy.

2. **Finished blog post** → `Business/[slug]/examples/YYYY-MM-DD_blog-post_[topic-slug].md`
   The final, publish-ready article itself, saved to the universal finished-copy archive.

Use today's actual date for `YYYY-MM-DD` (fill it in at run time if not otherwise known) and a short, readable slug for `[topic-slug]`.

## 7. Response behavior

**If the business isn't clear:** ask before writing anything — see Section 1, step 0.

**If given only a topic:** make reasonable assumptions about primary keyword and target audience segment, and produce a complete draft rather than asking first — state the assumptions at the top.

**If asked to optimize an existing post:** don't rewrite it wholesale — apply Sections 3 and 4 as a targeted pass and flag specifically what changed and why.

**After saving:** confirm both saves to the user, with the actual file paths — the content brief in `Business/[slug]/seo/` and the finished post in `Business/[slug]/examples/`.

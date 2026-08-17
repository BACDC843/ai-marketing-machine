---
name: brand-review
description: >
  Reviews any piece of marketing content — ads, captions, emails, scripts, landing pages, blog posts, any copy — against the business's brand voice, messaging pillars, and style guide, flagging deviations by severity with specific before/after fixes. Reads brand voice, audience, and honesty flags from your Business/[slug]/context/ folder at runtime rather than hardcoding any brand's standards. Use before publishing anything, when asked to check, audit, or QA a draft, or when a piece of content "doesn't feel right" and needs a second opinion against the brand standard. For content that doesn't exist yet, use the relevant content skill (social-creative-designer, carousel-post-designer, ad-creative-designer, ai-search-blog-writer, lead-magnet, or a repurposing skill) instead — this skill reviews, it doesn't originate.
---

# Brand Review

Every piece of content should pass through this skill before it ships. It's the one place in this project where "does this actually sound like the business" gets checked systematically, against that business's real, documented standard — not a generic notion of "good marketing copy."

Do not soften findings to be polite. A review that rubber-stamps everything isn't a review — the value here is catching what would otherwise ship off-brand or exposed to real risk (fabricated claims, an unsubstantiated testimonial, a compliance flag).

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

## 1. Determine the business, then read their standard

The active business is already resolved. Before doing anything else:

0. **Confirm the business profile.** The active business was resolved once at the top of this skill — don't re-resolve or re-ask here. If no profile exists yet, stop and run `business-setup` rather than writing against an empty context folder.

1. Read `Business/[slug]/context/brand-voice.md` — this is the review standard. Positioning, voice pillars, tone dial, vocabulary use/avoid, messaging framework, CTA toolkit, do's/don'ts.
2. Read `Business/[slug]/context/audience.md` — who the content needs to actually speak to, and what qualifies/disqualifies the right reader.
3. Read `Business/[slug]/context/products.md` — the real offer, and critically, any honesty flags (e.g. a business that's pre-revenue or pre-case-study and shouldn't have testimonial-style claims in its content yet).
4. Read the relevant `Business/[slug]/context/style-guides/` file for the content type being reviewed (`social.md` for a post, `ads.md` for ad copy, `blog.md` for an article, etc.) — platform/format-specific conventions live there, not in `brand-voice.md`.
5. Also check `Business/[slug]/examples/` for prior approved pieces of the same content type as the piece being reviewed — if any exist, use them as an additional calibration reference alongside `brand-voice.md`: what has already been judged good for your business. This folder may be empty for a business with no history yet — don't block on it, just note when it's not available. This is a read-only reference; brand-review does not write to `examples/` or anywhere else — it only reviews content the user provides.

**If `Business/[slug]/context/` is still an unfilled placeholder,** say so plainly — a review against a placeholder standard isn't a real review. Offer to proceed against general best-practice copywriting standards instead, clearly labeled as not a brand-specific check.

---

## 2. Review dimensions

Evaluate the content against each of these:

### Voice and tone
- Does the content sound like this specific business, not a generic version of "professional marketing copy"?
- Where does it sit against the tone dial documented in `brand-voice.md`, and does it match?
- Any hedging phrases, passive voice, or generic filler flagged as "avoid" in `brand-voice.md`?

### Positioning and audience alignment
- Does the content speak to the audience actually defined in `audience.md`, not a broader or different one?
- Does it reflect the brand's real positioning (premium/selective, plainspoken/accessible, or whatever your business's `brand-voice.md` actually documents — don't assume every business is positioned the same way)?
- If `audience.md` defines qualifiers (a budget signal, a segment marker), does the content include them where relevant?

### Messaging pillars
- Does the content reinforce at least one of your business's documented voice pillars?
- Are claims consistent with `products.md` — nothing promised that isn't real?

### Vocabulary and terminology
- Any words/phrases flagged as "avoid" in `brand-voice.md`'s use/avoid table?
- Are the business's actual power words/preferred vocabulary present where natural?
- Is the brand name used correctly and consistently?

### Structure and CTA
- Does the content open with a real hook, not a throat-clearing opener?
- Does it use the business's actual CTA toolkit from `brand-voice.md`, not a generic "learn more" / "contact us"?
- Exactly one clear CTA, not several stacked?
- For social content: does it match the hashtag/format conventions in `style-guides/social.md`?

### Honesty and compliance — always checked, regardless of business
- **Unsubstantiated claims**: superlatives ("best," "only," "fastest," "#1") without real evidence.
- **Fabricated or implied proof**: a testimonial, client story, or specific outcome number that isn't real. Cross-check directly against `products.md`'s honesty flags — if that file notes the business is pre-revenue or pre-case-study, treat any proof-style claim as an automatic high-severity finding.
- **Guarantee language**: "guaranteed," "promised," or similar, unless the business's own materials use this deliberately and it's legally sound for their industry.
- **Competitor references**: negative or comparative claims about named competitors.
- **Off-strategy channel use**: if a piece of paid ad copy is being reviewed, check `style-guides/ads.md` for whether paid is even an active channel for your business — flag if the content assumes a budget or channel that isn't actually live.

---

## 3. Output format

### Summary
- Overall assessment (1-2 sentences)
- Biggest strength (1-2 sentences)
- Most important improvement needed (1-2 sentences)
- Brand voice score: **Strong** / **Mostly on-brand** / **Needs work** / **Off-brand**

### Detailed findings

| Issue | Location | Severity | Suggestion |
|---|---|---|---|

Severity levels:
- **High** — contradicts brand voice, contains a compliance/honesty risk, or significantly undermines the message. Includes any fabricated-proof finding per Section 2.
- **Medium** — inconsistent with guidelines but not damaging.
- **Low** — minor style or preference issue.

### Revised sections

For the top 3-5 highest-severity issues:

**Before:** [original text]
**After:** [suggested revision applying your business's actual brand voice]
**Why:** [what was wrong, and how the revision fixes it]

### Honesty / compliance flags

List separately from the general findings table, with a recommended action for each — these shouldn't get lost among lower-stakes style notes.

---

## 4. Quality bar

- Every flagged word, tone note, or CTA issue traces back to something actually documented in `Business/[slug]/context/brand-voice.md` or `style-guides/`, not a generic copywriting opinion dressed up as a brand rule.
- Honesty/compliance findings are never softened or bundled in with minor style notes — they get their own section every time.
- The review doesn't invent a stricter or looser standard than the business's actual documented voice — if `brand-voice.md` is thin, the review says so rather than filling gaps with assumptions.
- Before/after revisions actually sound like the business, not like generic "improved" copy.

## 5. Response behavior

**If the business isn't clear:** ask before reviewing anything — see Section 1, step 0.

**If content is pasted, attached, or linked:** review it directly. If multiple pieces are given, review each separately rather than blending findings.

**If `Business/[slug]/context/brand-voice.md` is a placeholder:** say so, offer a general best-practice review instead, and recommend running `business-setup` before relying on brand-specific review for your business.

**After the review, ask:** "Want me to revise the full piece with these fixes applied, focus on just the high-severity issues, review another piece, or draft a brand-compliant replacement from scratch?"


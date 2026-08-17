---
name: landing-page-builder
description: >
  Designs and writes visually appealing, high-converting landing pages — section-by-section copy plus, on request, a self-contained coded HTML page — built to maximize conversions and cut friction. Reads brand voice, audience, products, and brand-board tokens from Business/[slug]/context/ at runtime rather than hardcoding any brand, covering opt-ins, paid checkout, book-a-call, waitlist, and webinar pages for any business. Use whenever the user asks for a landing page, opt-in page, sales page, squeeze page, or booking page, or wants a campaign, ad, lead magnet, or launch to have a dedicated page for traffic — even without saying "landing page," just wanting somewhere to send clicks or capture emails. If there's no clear offer yet, use ad-creative-brief or campaign-plan first. For the lead-magnet asset itself, use lead-magnet; for traffic-driving copy, use social-creative-designer, carousel-post-designer, or ad-creative-designer; for QA, use brand-review.
---

# Landing Page Builder

A landing page has one job: get the specific visitor who just arrived — from an ad, an email, a bio link — to take one specific action. Everything on the page either moves them toward that action or creates friction that costs conversions. Unlike a blog post or social caption, a landing page is judged almost entirely on what it does, not how nice it reads — so this skill is as much about structure, proof, and friction removal as it is about copy.

This skill produces both the strategic copy (section-by-section, always) and, on request, an actual coded page (self-contained HTML/CSS, mobile-first) — see Section 7. It doesn't set campaign strategy (`ad-creative-brief`, `campaign-plan` do that), doesn't write the gated asset itself (`lead-magnet` does that), and doesn't write the ads/posts that drive traffic here (`social-creative-designer`, `carousel-post-designer`, `ad-creative-designer` do that). It also doesn't render social graphics or export PNGs — `graphic-production-studio` owns that pipeline; this skill owns full page layouts.

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
2. Read `Business/[slug]/context/brand-voice.md` — tone, approved language, words to avoid. A landing page in the wrong voice undermines the exact trust it's trying to build.
3. Read `Business/[slug]/context/audience.md` — pain points, objections, decision triggers, the language they actually use. Landing page copy should mirror the visitor's own words back at them, not marketing-speak.
4. Read `Business/[slug]/context/products.md` — the real offer, real pricing, real deliverables. A landing page that oversells what's actually offered creates refunds, chargebacks, or an audience that churns immediately — worse than a page that underperforms honestly.
5. Read `Business/[slug]/context/style-guides/landing-pages.md` if it exists and isn't a placeholder — page structure, headline conventions, the single-conversion-action rule, proof conventions, and copy-length constraints already decided for your business. If it's still an unfilled placeholder, say so and proceed on the general principles in this skill.
6. Read `Business/[slug]/context/brand-board.md` — colors, typography, logo rules, and (if filled in) the **CSS starter tokens** block. If you're producing a coded page (Mode B, Section 7), use these tokens directly rather than inventing a palette. If `brand-board.md` is still a placeholder, say so and build with a clean, neutral system instead of guessing at brand colors.
7. Check `Business/[slug]/examples/` for prior landing pages before writing new ones, and treat any found as calibration examples of already-approved structure and voice.

**If any context file is still an unfilled placeholder,** say so plainly in the output, then proceed on reasonable defaults inferred from the offer and the general principles below. Don't block the request over missing context — a placeholder brand-board just means the coded output uses a clean neutral system instead of the business's real colors.

---

## 2. Gather what the page actually needs before writing a word

A landing page's whole value is in getting these specifics right — vague inputs produce a vague page, no matter how well the sections are structured. Before writing, make sure you actually know:

- **The goal.** What's the one action? (email opt-in, paid checkout, book-a-call, waitlist join, webinar registration, quote request.) This determines the page shape — see Section 3.
- **The offer.** What does the visitor get, specifically, and what do they give in return (money, email, a call)? Pull this from `products.md` — don't let the page promise something the offer doesn't actually deliver.
- **The price** (if there is one), and how it should be framed (one-time vs. subscription, anchored against a comparison, a limited-time element if genuinely true).
- **The primary CTA wording** — what the button should say, and where it should point (a Stripe link, a booking calendar, a form).
- **Objections.** What's the visitor's real hesitation? ("Is this for someone like me?" "Will this actually work?" "What if I want a refund?") Pull from `audience.md` if it documents these; if not, infer the 2-3 most obvious ones for this offer and address them directly rather than leaving them unspoken.
- **Proof available.** Real testimonials, real results/data, a real screenshot, a real credential — whatever actually exists. Never fabricate a testimonial, a number, or a screenshot. If no real proof exists yet, say so and either build the page without a fabricated proof section or flag it as the single biggest thing to fix before this page should go live.
- **Traffic source.** A visitor arriving cold from a paid ad needs more context and trust-building than someone clicking from an email that already warmed them up. Ask or infer this — it changes how much the hero and early sections need to re-establish who this is and why it matters.

If the goal or the offer is unclear, ask — building the wrong page shape wastes more time than a clarifying question. If proof, objections, or traffic source are unclear, make a reasonable assumption, state it plainly at the top of the output, and move on.

---

## 3. Match the goal to a page shape

Not every page needs every section in Section 4 — a free opt-in page with a heavy pricing/comparison block is itself a friction point (it makes a free thing feel like it has a catch). Use this as a starting map, not a rigid rule:

| Goal | Hero | Trust signals | Demo | Problem/solution | Proof | Testimonials | What's included | Pricing | Changelog | Audience fit | FAQ | Final CTA | Secondary offer |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Paid checkout** (course, product, service package) | required | required | strong if possible | strong if possible | required | required | required | required | optional | required | required | required | strong if possible |
| **Lead-gen opt-in** (free guide, checklist, waitlist) | required, lighter | required | optional | optional | optional | if available | optional (what's inside the freebie) | skip — it's free, don't frame it like a sale | skip | optional | short version | required | not applicable — the opt-in IS the low-commitment offer |
| **Book-a-call / consultation** | required | required | optional | strong — this is often the whole page | if available | required | skip | skip or "what to expect on the call" | skip | required — pre-qualifies who should book | required — handles "what happens on this call" objections | required | optional — a lower-commitment resource for people not ready to book |
| **Webinar / event registration** | required, date/time prominent | required | optional | strong | if available | if available | "what you'll learn" in place of "what's included" | skip unless paid event | skip | optional | required | required | optional — replay/recording opt-in for people who can't attend live |

Adapt this rather than treating it as exhaustive — the underlying question for every section is always "does this move the specific visitor toward the one action, or is it here because a template said so?"

---

## 4. The section toolkit

Each of these is a proven pattern, not a mandatory checklist — use Section 3 to decide what this specific page needs.

1. **Hero** — headline, subheadline, the offer/price if relevant, and the single primary CTA, all visible without scrolling. The headline should state the outcome or transformation in the audience's own language, not a feature list. This is the only guaranteed-read section — if it doesn't earn the scroll, nothing below it matters.
2. **Trust signals** (immediately under the hero) — a short, real credibility line: who's behind this, a rating, logos of where it's been featured, a small row of real customer photos. This exists to answer "why should I trust this" in under two seconds, before any argument has been made.
3. **Product-in-action demo** — show the thing working, concretely: a screenshot, a short mocked-up interaction, a before/after. Concrete beats abstract every time — "here's what it actually looks like" outperforms "here's what it can do for you."
4. **Problem/solution comparison** — "Without this" (pain, marked ✕) next to "With this" (relief, marked ✓). This works because it makes the visitor's current frustration explicit before offering the fix — skipping straight to the fix without naming the pain undersells the offer.
5. **Proof** — real data, a real result, a real screenshot, explicitly labeled as real ("this isn't a mockup — this is our actual [X]"). Vague claims ("results that speak for themselves") are worse than no proof section at all; specific, labeled proof is what actually moves a skeptical visitor.
6. **Testimonials** — photo, a quote with the single most important phrase bolded, name, and a role/credential that makes the quote credible for this specific audience. Never write a testimonial that doesn't exist — ask the user for real ones from `Business/[slug]/examples/` or client-supplied material, or skip the section and flag it as missing.
7. **What's included** — a scannable checklist, grouped by category if the offer has several parts, followed by a short "everything you get" recap right before the CTA. This does double duty: it answers "what exactly am I getting" and it's also skimmable filler that a scanning visitor can absorb in a few seconds.
8. **Pricing** — one clear price, framed against a comparison or anchor if one genuinely exists (cost of the alternative, cost of doing nothing, a reasonable per-unit breakdown) — never an invented "was $X, now $Y" unless that discount is real. Repeat the primary CTA right here.
9. **Changelog / momentum** (optional) — recent updates, what's new, proof the thing is alive and actively improving. Skip this for anything without a real update history; a fabricated changelog is worse than no changelog.
10. **Audience fit** — a "this is built for X, Y, Z" list paired with an honest "this is NOT for..." list. The second list feels counterintuitive (why talk anyone out of buying?) but it does real work: it pre-qualifies visitors, reduces refunds/mismatched signups, and the honesty itself builds trust that the rest of the page's claims are also straight.
11. **FAQ** — real objections, answered in a conversational tone, not corporate hedging. Pull the actual questions from Section 2's objections list rather than generic filler ("Is this secure?" for a $19 checklist is filler; "What if this doesn't fit my industry?" is a real objection worth answering).
12. **Final CTA** — repeat the offer, the price if relevant, and any real risk-reversal (guarantee, refund policy, "cancel anytime") one more time. This is for the visitor who scrolled the whole page and is ready to act now — don't make them scroll back up to find the button.
13. **Secondary offer / low-commitment path** — for visitors who read the whole page and still aren't ready for the primary action, a smaller ask (a free resource, a newsletter signup, a shorter/free version of the offer) captures them instead of losing them entirely. This matters most on paid-checkout and book-a-call pages, where the primary ask is high-commitment.

---

## 5. Copy principles — conversion and friction reduction

- **One primary CTA per page.** Every button on the page should point at the same action, worded consistently. A page offering "Buy Now" and "Learn More" and "Book a Call" as equally-weighted options isn't reducing friction, it's outsourcing the decision the page should have already made.
- **Remove friction wherever it isn't earning its keep.** Every form field costs conversions — ask only for what's truly needed for the very next step (an email for an opt-in, not an email + phone + company size + how-did-you-hear-about-us). Every extra click, every unclear next step, every unanswered "wait, what happens after I click this" is friction.
- **Address objections inline, not just in the FAQ.** If a visitor would hesitate at a specific section (price, a bold claim, "is this for me"), answer it right there in a supporting line rather than hoping they scroll to the FAQ before bouncing.
- **Specific beats vague, always.** "5.77K clicks, 890K impressions, last 6 months" beats "amazing results." "Built for solo marketers doing their own SEO, content, and social" beats "perfect for everyone." Pull real specifics from `products.md`, `audience.md`, and whatever proof the user supplies — never invent a specific-sounding number to fill a gap.
- **Write for the scan, not the read.** Assume most visitors skim before they decide whether to actually read. Short paragraphs (1-3 lines), bolded key phrases within testimonials and body copy, checklists over prose, and generous whitespace all serve the same goal: the page's argument should be graspable from a skim alone.
- **Mobile is the default reading context**, not an afterthought — most landing page traffic from ads and social arrives on a phone. Write headlines and body copy short enough to hold their meaning in a narrow single-column layout, and keep the primary CTA within easy thumb reach.

---

## 6. Building the coded page

When producing Mode B (Section 7), the page should be a single self-contained HTML file — inline CSS, no external CDN dependencies, no build step — so it can be opened directly or dropped into any host.

- Pull real color and font values from `Business/[slug]/context/brand-board.md`'s **CSS starter tokens** block and use them as CSS custom properties (`:root { --color-primary: ...; --font-heading: ...; }`). If that block is empty, use a clean, neutral, professional system instead of guessing at brand colors — and say so.
- Design mobile-first: build the single-column layout first, then add wider breakpoints, not the reverse.
- Every section from Section 4 that's included should be its own clearly separated block — generous vertical spacing between sections is what makes a long page feel scannable instead of dense.
- Real images referenced from the business's own material (`Business/[slug]/examples/` or `Business/[slug]/visuals/`) can be linked directly; for anything without a real asset yet, use a clearly-labeled placeholder block (e.g., a bordered box reading "[testimonial photo]") rather than a stock photo that could be mistaken for something real.
- Forms should point at a placeholder or the real endpoint the user supplies (e.g., a GoHighLevel form action, a Stripe link) — never wire up a live payment or data-collection endpoint without the user explicitly providing it.

---

## 7. Output modes

### Mode A — Copy & structure blueprint (default)
Produce the full section-by-section copy per Section 4's applicable sections (per Section 3's goal mapping), in the markdown format in Section 8. This is the right default whenever the offer, angle, or proof points haven't been locked yet — it's fast to review and revise before any code gets written.

### Mode B — Coded page
Once the blueprint is approved (or immediately, if the user explicitly asks to skip straight to a built page and the inputs from Section 2 are clear), produce the self-contained HTML page per Section 6, implementing the approved copy.

### Mode C — Approval-first angle options
When the user is choosing between angles or isn't sure of the hook yet, don't write a full page. Instead give 2-3 headline/subheadline/primary-CTA combinations with a one-line rationale each, and stop for approval before expanding the winner into Mode A.

---

## 8. Output format — copy blueprint

```markdown
# Landing Page — [working title]

**Business:** [business slug]
**Goal:** [lead-gen opt-in / paid checkout / book-a-call / webinar / etc.]
**Primary CTA:** [exact button wording + destination]
**Traffic source assumption:** [paid ad / email / organic / bio link — state if assumed]

## Hero
**Headline:** ...
**Subheadline:** ...
**Offer/price line:** ...
**CTA button:** ...

## Trust signals
...

## [continue through each applicable section from Section 4, in the order chosen for this page]

## FAQ
**Q:** ...
**A:** ...

## Final CTA
...

## Secondary offer (if applicable)
...
```

Note under the title which Section 4 sections were deliberately skipped and why, per the Section 3 mapping — this keeps the reasoning visible for review instead of silently dropping sections.

---

## 9. Quality bar — check before calling it done

- There is exactly one primary action on the page, worded and linked consistently everywhere it appears.
- The hero communicates the offer and the action clearly without requiring a scroll.
- At least one real proof element exists, or its absence is explicitly flagged as the top thing to fix before launch.
- The 2-3 most likely objections (Section 2) are answered somewhere on the page, not left for the visitor to wonder about.
- Copy reads as skimmable on a phone-width column: short paragraphs, bolded key phrases, no dense walls of text.
- Every claim, number, testimonial, and price traces back to something real in `products.md`, `audience.md`, or user-supplied material — nothing was invented to fill a gap.
- Tone matches `Business/[slug]/context/brand-voice.md`.
- If Mode B was produced, the coded page uses the business's real `brand-board.md` tokens (or plainly states it didn't have real ones to use).
- If any context file was incomplete, that's noted in the output rather than papered over.

---

## 10. Save Your Output

Once the blueprint (Mode A) is finished — and the coded page (Mode B) too, if produced — save automatically, without asking "should I save this?" first.

Save both the blueprint (`YYYY-MM-DD_landing-page_[slug].md`) and, if built, the coded page (`YYYY-MM-DD_landing-page_[slug].html`) to `Business/[slug]/examples/` — not `Business/[slug]/visuals/`, which is reserved for `graphic-production-studio`'s own rendered assets. Append a row to `Business/[slug]/social/content-calendar.md` with columns `Date | Format | Channel | Summary | Status | File`.

**Delivering the coded page.** Writing the `.html` into `examples/` *is* the delivery. State its full path, and confirm the write before you report it — never report a path you did not verify. If this surface can also display or attach the file, do that after it is written; if it can't, say nothing about it. Do not call a tool to hand the file over unless you have confirmed that tool exists in this session; assume none does. In `storage_mode: dropbox` the `.html` is text and goes through the connector normally.

Use today's real date when known; if it isn't known at run time, flag the placeholder plainly rather than guessing. If the user requests edits after saving, update the saved file(s) in place (in Dropbox mode there is no in-place append — fetch current content, edit, then delete and recreate) rather than creating duplicate files or duplicate calendar rows.

---

## 11. Response behavior

**If the business isn't clear:** ask before writing anything — see Section 1, step 0.

**If the goal or offer is unclear:** ask — see Section 2. Don't guess on these two; everything else can be a stated assumption.

**If given a clear offer and goal but nothing else:** make reasonable assumptions on proof, objections, and traffic source, state them at the top of the output, and produce a complete Mode A blueprint rather than stalling on questions.

**If asked to "just build the page" with no blueprint step:** skip straight to Mode B, using reasonable section choices per Section 3 — but still state assumptions plainly.

**If asked for options or "not sure of the angle yet":** use Mode C and stop for approval before expanding.

**If asked for edits:** change only what was flagged; don't rebuild sections that weren't called out.

**Once the page is finished and saved (Section 10):** confirm in the closing response that it saved, with the exact path(s).

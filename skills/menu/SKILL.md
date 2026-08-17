---
name: menu
description: >
  The front door to AI Marketing Machine. Renders a clickable start menu of the marketing jobs this system does (social post, carousel, week of content, blog, paid ad, campaign, business profile setup, performance, and more), then routes the click straight into the right specialist skill. Use when the user opens a session and says "AI Marketing Machine," "marketing menu," "start," "what can you do," "show me my options," "help me make something," "I need to post something," or any request that's clearly marketing work but doesn't name a format. Also use when they name two or more possible jobs and need to choose. Do NOT use when the request already names one job clearly — go straight to that skill instead; the menu is for picking, not for confirming a choice already made.
---

# AI Marketing Machine — Menu

This is the router. It exists so the user has one thing to remember instead of twenty-three skill names. Its job is to show the menu, capture a choice, and hand off. It does not produce marketing content itself — every piece of real work happens in a specialist skill.

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

## The bypass rule — read this before rendering anything

**Do not render the menu if the request already names the job.** "Write me an Instagram post about the new kitchen project" needs no menu — that is `social-post-pack`, run it. Showing a menu to someone who already told you what they want is friction, not helpfulness.

Render the menu only when:

- The request is a broad opener — "AI Marketing Machine", "let's do marketing", "what can you do", "start", "menu"
- The request names a topic but no format — "I need something for this week"
- The request could reasonably be two or more different jobs — "make something about the new project" (post? carousel? ad? week of content?)
- The user explicitly asks for the menu

**Two openers route straight past the menu:**

- **"help me post something", "I want to start posting", "write me a post but I don't know what about"** — a beginner with no plan. Go to `content-coach`, which walks brand capture, ideas, drafting, grading, and scheduling in one conversation. A twenty-one item list is the wrong answer to "I don't know where to start."
- **"how do I start", "I'm stuck", "what should I do this week"** — go to `getting-started`.

If you're between the two, do the work and mention the menu in one line at the end rather than blocking on it.

## 1. Confirm the business profile exists

This is a single-business workspace. There is no selector and no chip row — the menu opens straight into the job list.

1. Resolve the active business per the resolution block above: `aimm-config.md` (`business:`), or the single folder under `Business/` that isn't `_template`.

2. **If no profile exists at all, this is a first run.** Do not render the job list — a list of twenty-one jobs is a worse first impression than a sentence and a start.

   **This is the one signal for "fresh install" across the whole product:** no resolvable business profile under `Business/`. `business-setup` and `doctor` both defer to it, so all three agree.

   Say, in about two lines: welcome, that nothing can be written on-brand until it knows the business, and that setting up takes a few minutes and starts with their website. Then **go straight into `business-setup`** — don't ask permission, and don't show the menu first. `doctor` reports this same state but never acts on it; the menu is the one that routes.

3. If several folders exist and the config is silent, ask once which one this session is for, then carry that answer through the whole run without asking again.

## 2. Render the menu — widget where it renders, text everywhere else

**Decide which one you can actually render before you render anything.** A widget that doesn't render leaves an empty turn — the user asked a question and got nothing back. That is the worst outcome here, worse than a plain list.

**Decide by probing for the renderer, not by guessing from the surface.** Search for a widget-rendering capability — never by a literal `mcp__…` name, since the identifier differs between installs. Then:

- **A renderer resolves, and the surface is the desktop app** → widget (2a).
- **Anything else** → text menu (2b).

Surface type alone is not the test, and this is the specific failure worth avoiding: a desktop session where the renderer is *absent* passes a surface check and then renders nothing. Probing presence catches that; assuming from the surface does not.

Take 2b as well if `assets/menu-widget.html` cannot be read for any reason. A missing renderer or a missing asset is never a reason to leave the user with no menu — and the text menu is a first-class path, not a consolation prize.

### 2a. Widget — desktop only

1. Probe for the widget renderer **silently** — never narrate the call. If it isn't there, go to 2b without comment.
2. Read `assets/menu-widget.html` from this skill folder.
3. Render it with `title: "ai_marketing_machine_menu"`. The widget carries no business name and needs no substitution.
4. Keep your text response to **one or two lines**. The menu carries the explanation. Do not restate the options in prose underneath — that defeats the entire point.

### 2b. Text menu — mobile, web, or missing asset

Same jobs, same routing, no HTML. One message, nothing above it:

```
 1. Social post — copy, caption, and a finished graphic
 2. Carousel post
 3. A full week of social content
 4. Blog post — SEO and AI search
 5. Paid ad
 6. Full campaign plan
 7. Set up or update my business profile
 8. Check social performance
 9. Browse content templates
10. SEO and local SEO audit
11. Lead magnet
12. Landing page
13. Repurpose an existing piece of content
14. Review a draft against brand voice
15. Schedule an approved post
16. Portfolio report from a website URL
17. Help me post something — I don't have a plan yet
18. Quick brand setup — six questions
19. Check what's set up and what's missing
20. How do I get started, or I'm stuck
21. Something else — just describe it

Reply with a number — "3" — or plain English. Both work.
```

Keep this order identical to the routing table in step 3 so the numbers stay stable between runs and the user can learn them. A number that arrives on its own routes exactly like a card click.

Do not use `AskUserQuestion` for either version. It caps at four options per question, which is why this menu exists as a widget and a plain list rather than a prompt.

## 3. Route the click

Clicking a card fires `sendPrompt()`, which arrives as a normal user message. Route it using this table. When more than one skill is listed, run them in order and carry the output forward without asking between steps.

| What comes back | Skill to run |
|---|---|
| Create a social post — copy, headline, caption, hashtags, and a finished branded graphic | `social-post-pack` |
| Build a carousel post | `carousel-post-designer` → `graphic-production-studio` |
| Plan and produce a full week of social content | `weekly-content-plan` |
| Write a blog post optimized for SEO and AI search | `ai-search-blog-writer` |
| Make a paid ad | `ad-creative-brief` → `ad-creative-designer` |
| Plan a full marketing campaign | `campaign-plan` |
| Set up or update my business profile | `business-setup` |
| Check social performance | `performance-digest` |
| Browse content templates | `templates` |
| Run an SEO and local SEO audit | `seo-audit` |
| Create a lead magnet | `lead-magnet` |
| Build a landing page | `landing-page-builder` |
| Repurpose an existing piece of content | ask which channel, then `repurposing-to-instagram`, `repurposing-to-linkedin`, or `repurposing-to-newsletter` |
| Review a draft against brand voice | `brand-review` |
| Schedule an approved post | `post-scheduler` |
| Build a full marketing portfolio report from a website URL | `website-portfolio-report` |
| Help me post something — I don't have a plan yet | `content-coach` |
| Quick brand setup — six questions | `brand-brief` |
| Check what's set up and what's missing | `doctor` |
| How do I get started, or I'm stuck | `getting-started` |
| Free-text from the "Something else" box | read the intent and pick from the full skill set; if it maps to nothing, say so plainly rather than forcing a fit |

One special case: **no business profile yet** — that is a first run; see step 1. Route into `business-setup` rather than producing content against an empty context folder.

**The order of this table is load-bearing.** It must match the numbered list in 2b position for position, because a bare number routes by counting rows here. They drifted apart once — `doctor` sat at position 8 in this table and 17 in the list, silently mis-routing every number from 8 to 16. `_scripts/verify_decoupling.py` now checks the correspondence on every run; if you add a row, add the matching list item in the same position.

### Deliberately not carded

`post-writer`, `post-grader`, and `social-creative-designer` have no menu entry **on purpose**. They are invoked by other skills — `social-post-pack` and `weekly-content-plan` run them as steps — and a user has no reason to pick them directly. They remain invocable by name. This is recorded so the absence reads as a decision rather than an oversight, and so the parity check knows not to flag them.

## 4. Collect the job spec — one form, not a Q&A

Most jobs need a few settings before work starts: platform, format, topic, links. **Do not ask for these in a back-and-forth.** One screen, defaults pre-selected.

The same surface rule from step 2 applies. **Desktop app** → render `assets/spec-widget.html` (4a). **Mobile, web, unknown, or a missing asset file** → the text spec (4b).

### 4a. Spec widget — desktop only

1. Read `assets/spec-widget.html`.
2. Replace the `/*CONFIG*/` token **and the object literal immediately after it** with a JavaScript object for this job (schema below). Replacing only the token leaves two object literals side by side — `var CONFIG = {…yours…}{…fallback…};` — which is a syntax error and renders a blank widget. The fallback exists so the file is valid on its own; it is not meant to survive substitution.
3. Render it with `title: "amm_spec_[job]"`.
4. Say **nothing** except at most one line. The form is the message.

Config schema:

```js
{
  title: "Create a Social Post",
  subtitle: "Anything you skip, I'll pick a sensible default.",
  submitNote: "Takes about a minute.",
  intro: "Create a social post with these settings:",
  fields: [
    { id: "platform", label: "Platform", required: true,
      options: ["Instagram", "Facebook", "LinkedIn", "All three"], default: 0 },
    { id: "ratio", label: "Image ratio",
      options: ["4:5 Vertical", "1:1 Square", "9:16 Story/Reel", "1.91:1 Landscape"], default: 0 },
    { id: "visual", label: "Visual style", hint: "How the graphic gets made.",
      options: ["Designed text card", "My photo + headline", "AI-generated scene"], default: 0 },
    { id: "topic", label: "Topic or angle", type: "text", required: true,
      placeholder: "e.g. the autumn kitchen reveal",
      hint: "Or type 'you pick' and I'll propose three from your brand context." },
    { id: "extra", label: "Anything else", type: "textarea",
      placeholder: "Paste links, photo paths, offers, dates, notes — whatever you have.",
      hint: "Optional. Links, docs, screenshots, or details all work." }
  ]
}
```

Field types: omit `type` for a chip row, `"text"` for one line, `"textarea"` for a block. Chip rows get an "Other" chip with an inline input automatically — set `allowOther: false` to suppress it. `default` is the zero-based index to pre-select.

**Build the field list for the job, not from a template.** A blog post needs target keyword and length, not image ratio. A campaign needs duration and budget. An SEO audit needs a URL and competitors. Four to six fields is right; more than seven means the form is doing the skill's job.

### 4b. Text spec — mobile, web, or missing asset

Ask the same fields as one compact numbered block in a **single message**, with every default stated so the user can accept them all with one word:

```
Creating a social post. Defaults in brackets — reply with just
the ones you want to change, or say "go" to take them all.

1. Platform [Instagram]
2. Image ratio [4:5 vertical]
3. Visual style [designed text card]
4. Topic or angle — needed. Or say "you pick" and I'll propose three.
5. Anything else? Links, photo paths, offers, dates.
```

Rules that make this work on a phone: every field except the genuinely required one carries a default, "go" accepts all of them, and short replies like `1 LinkedIn, 4 the autumn kitchen reveal` are valid. Never ask these one at a time — a five-turn interrogation on mobile is worse than the widget not rendering.

**Skip the form entirely** — either version — when the click or the request already carried everything. A spec form asking questions the user just answered is the same friction as a menu they didn't need. Also skip it for `business-setup` and `website-portfolio-report`, which run their own intake.

## 5. Hand off cleanly

When the form comes back, invoke the specialist skill directly. Do not summarize what the skill is about to do, do not ask "shall I proceed," and do not re-ask for anything the form already carried. One short line of acknowledgement at most, then the work.

If something is still genuinely missing, ask for **only** that one thing.

## 6. Quality bar

- The menu appears within the first response of a qualifying request — never after a paragraph of preamble.
- Menu → spec form → work. Never more than two widgets before real output starts.
- No widget is ever rendered to confirm something the user already said.
- Every card leads to a real skill that exists in this plugin. If a skill is removed, remove its card in the same pass.
- No menu is ever shown twice in a row. If the user is already mid-job, stay in the job.

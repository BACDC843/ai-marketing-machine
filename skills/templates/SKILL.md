---
name: templates
description: >
  Browsable gallery of content structures — hook shapes, slide skeletons, and render presets for single posts, carousels, paid ads, and reveals — so no piece of content starts from a blank page. Renders a filterable card gallery; picking a template hands its skeleton to the right production skill, which then fills it from Business/[slug]/context/. Use when the user asks to see templates, browse the template gallery, wants "a proven format," asks "what should I post" without a topic, says they're stuck or staring at a blank page, or wants to reuse the structure of something that worked before. Also use to add a new template after a piece performs well. Does not write content itself — it supplies the skeleton and hands off to social-post-pack, carousel-post-designer, ad-creative-designer, or weekly-content-plan.
---

# Templates

A structure library. Every entry is a shape that has either been produced and graded in this system or is a standard, well-understood format — never filler invented to pad a count.

**Templates hold structure, never brand values.** A template says "hook with a specific number, then the assumption, then the mechanism." It never says what the number is, what voice to use, or what colors to render in. Those come from `Business/[slug]/context/` at runtime, exactly as they do everywhere else in this project. A template that hardcodes a brand value is a bug.

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

## 1. Show the gallery — widget on desktop, text everywhere else

**Decide by probing for the renderer, not by guessing from the surface.** Search for a widget-rendering capability — never by a literal `mcp__…` name, since the identifier differs between installs. Use 1a only when a renderer actually resolves *and* the surface is the desktop app. Use 1b for everything else, including a desktop session where the renderer turns out to be absent — that case passes a surface check and then renders nothing, which is the failure worth avoiding. Take 1b as well if `assets/gallery-widget.html` can't be read.

### 1a. Gallery widget — desktop only

1. Read the template library: try `Templates/templates.json` at the **project root** first (that's where §4 writes additions), and fall back to the bundled `library/templates.json` inside this skill's folder. If both exist, merge them, with the project-root entries winning on duplicate `id`.
2. Read `assets/gallery-widget.html`.
3. Replace the `/*DATA*/` token **and the object literal immediately after it** with the JSON. Replacing only the token leaves two literals side by side — `var DATA = {…yours…}{ categories: [], templates: [] };` — which is a syntax error and renders a blank widget. Same rule for `/*FILTER*/` and the `'all'` that follows it.
4. Render with `title: "amm_template_gallery"`. (The renderer was already probed in step 1 — don't probe twice.)
5. Say at most one line. The gallery is the message.

### 1b. Text gallery — mobile, web, or missing asset

Read the template library the same way as 1a (project-root `Templates/templates.json` first, then the bundled `library/templates.json`, merged) and list the templates as a numbered set, grouped by category, one line each: the template name, then a short clause on what it's for. Cap it at the strongest ~12 unless the user asked for everything — a phone screen is not a gallery wall, and an exhaustive dump is harder to choose from than a curated one. Close with: *"Reply with a number."* Say which categories you trimmed if you trimmed any.

If the user named a category ("show me carousel templates"), filter to it in both versions — pass `/*FILTER*/` as that category id for the widget, or list only that category in the text version.

## 2. Route the pick

Clicking a template fires `sendPrompt()` with the template name and id. Then:

1. Read that template's entry from the merged library (see step 1).
2. Hand off by `category`:

| Category | Skill |
|---|---|
| `post` | `social-post-pack` |
| `carousel` | `carousel-post-designer` → `graphic-production-studio` |
| `ad` | `ad-creative-brief` → `ad-creative-designer` |
| `other` | `social-post-pack`, unless the entry says otherwise |

3. Pass the template's `hook`, `skeleton`, `render`, and `cta` into that skill as the structure to fill. The production skill still does everything it normally does — reads context, grades, renders, saves. The template replaces the blank page, not the process.
4. If the entry has a `warning`, apply it as a hard constraint and state it in the output. Those exist because the shape has a specific way of going wrong.

**A template is a starting shape, not a cage.** If the business's context makes a slot wrong — a `selectivity` post for a business that needs every lead it can get — say so and pick a better template rather than filling it anyway.

## 3. Topic

Templates supply structure, not subject. If the request carried a topic, use it. If not, read `Business/[slug]/social/content-calendar.md` and `context/` and propose **three** angles that fit the chosen shape, then let the user pick. Do not ask an open "what should this be about?" — propose.

## 4. Adding a template

When a piece performs well, its shape is worth keeping. Add an entry to `library/templates.json` with:

- `id` (kebab-case), `name`, `category`, and `slides` for carousels
- `when` — the situation this shape is *for*, in one sentence. This is the field that makes the gallery useful; a vague `when` makes a template unpickable.
- `hook` — the hook shape with `[bracketed]` slots
- `skeleton` — the beat-by-beat structure
- `render` — `layout` (`editorial` / `quote` / `photo-overlay`) and `ratio`
- `cta` — `save` / `comment` / `dm` / `link` / `download` / `soft`
- `warning` — optional, for shapes with a known failure mode

Also update `updated` at the top of the file.

**Where the new entry goes.** `library/templates.json` ships *inside the installed plugin* — writing there is lost on the next plugin update, and on mobile it isn't writable at all. Write additions to a workspace-root copy at `Templates/templates.json` instead, and in Section 1 read that copy first, falling back to the bundled file when it doesn't exist. If neither is writable, say the template wasn't saved rather than reporting a success — a silently discarded template is worse than a refusal.

**Promotion rule:** only add a shape once a real piece built from it scored 8.0+ *and* shipped. A high grade alone is a draft, not a template worth reusing. Once `performance-digest` writes measured engagement back into the content calendar, prefer real performance over the grade.

## 5. What this skill does not do

- It does not write copy, choose topics, or render images.
- It does not store brand colors, fonts, voice, or logo rules — `brand-board.md` and `brand-voice.md` own those.
- It does not gate anything. The user can always ignore the gallery and describe what they want; templates are a shortcut, not a required step.

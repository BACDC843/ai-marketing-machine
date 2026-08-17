---
name: doctor
description: >
  Checks this installation and reports, in plain English, what is working, what is missing, and what each missing piece actually costs — covering the business profile itself (is the brand context real, still placeholder text, or unconfirmed starter-pack defaults) plus storage, graphics, publishing, performance data, and the menu. Probes everything live rather than trusting a previous session, then writes what it found to .aimm/environment.md so other skills can see it. Use when the user asks what's wrong, why something isn't working, what's set up, what they still need to connect, whether they're ready to start, or after an install or a failed run. Also runs at the end of business-setup. Reports only — it never changes a setting, installs anything, or fixes what it finds.
---

# Doctor

A check-up, written for the person who owns the business, not the person who built the software.

Two questions get answered: **is your brand set up properly**, and **what is this installation actually able to do right now**. Every finding says what it costs you, because "Blotato: not connected" means nothing on its own and "you'll copy and paste each post yourself" means something.

---

## Workspace and file access — resolve this before any read or write

Every `Business/...`, `memory.md`, and other workspace path in this skill is relative to your workspace root. Resolve it **once** at the start of the run, then use the same method for every read and write that follows:

1. **The current project folder is the workspace root.** If a folder is open or mounted in this session, that folder is the root. This is the default and needs no configuration.
2. **`aimm-config.md` at that root can override it.** If it sets `workspace_root`, use that path instead. If it sets `storage_mode: dropbox`, read and write through the Dropbox tools at that path. Dropbox is used only when the config says so, and only at the path the config gives — never a built-in one.
3. **Nothing reachable.** Say so in one line and ask which folder to use. For this skill that is itself a finding — report it as "I couldn't find your files" rather than failing silently.

**Plugin-relative paths are the exception.** Paths beginning `assets/`, `scripts/`, `library/`, or `references/` live inside a skill's own folder in the installed plugin — not in the workspace root and not in Dropbox.

**Finding a connector:** always by **capability, not by name**. Connector prefixes differ between installs — the same server can appear as `mcp__Blotato__…`, `mcp__claude_ai_Blotato__…`, or something else. Search for the capability and use whatever resolves. **Never match a literal `mcp__…` string, and never report a connector as absent because one guessed name failed.** This is the single most common way a check like this lies.

---

## The rules this skill runs on

1. **Probe every time. Trust nothing from a previous run.** Renderers, connectors, and MCP availability have all changed between sessions on the same machine. `.aimm/environment.md` is this skill's *output*, never its input.
2. **"Not applicable here" is not "broken."** Chromium has no place on a Windows install; saying "missing" would send someone chasing a fault that does not exist. Use three states only: **working**, **not connected**, **not applicable here**.
3. **Never fix anything.** Not a setting, not an install, not a file. Report, and say what fixing it would involve. If the user then asks you to fix something, that is a new request — run the skill that owns it.
4. **Never invent a cost.** If you genuinely don't know what a gap costs, say what it blocks and stop there.
5. **No jargon in the report.** "Saving files", not "storage_mode". "Making graphics", not "the Pillow render path". Technical names belong in `.aimm/environment.md`, not in what the user reads.
6. **Confirm before reporting.** Same rule every other skill follows: never state a file exists, or a tool works, without having actually checked in this run.

---

## 1. Check the business profile

Resolve the active business first. If **no profile exists at all**, that is the headline finding — report it, say nothing else can produce on-brand work until it exists, point at `business-setup`, and skip to Section 2. Do not treat an empty workspace as an error; it is the expected state on a fresh install.

Otherwise read each file under `Business/[slug]/context/` and classify it:

- **Real** — filled in with this business's actual details, confirmed by the owner.
- **Starter-pack default** — contains `[starter-pack default]` markers. Trade-typical text that was seeded during setup and never confirmed. **This is not the same as filled and not the same as empty**, and reporting it as either is the most misleading thing this skill could do: the file looks complete, reads plausibly, and is about a generic business rather than this one.
- **Still placeholder** — contains `Status: not yet filled in`, or its content is still the bracketed `[hints]` from the template.
- **Missing** — the file isn't there.

Check all four context files (`brand-voice.md`, `audience.md`, `products.md`, `brand-board.md`) and all seven under `style-guides/`. Also check whether `social/content-calendar.md` exists.

**What each gap costs** — use these, they are the point of the section:

| Still placeholder | What it costs |
|---|---|
| `brand-voice.md` | Everything written sounds like generic marketing copy. This is the file that makes content sound like *you*, so it is the most expensive gap on this list. |
| `audience.md` | Posts talk about the business instead of to the customer. Hooks land flat because nothing names a real frustration. |
| `products.md` | Content can't name a real offer or price, and can't be trusted not to over-claim. Its honesty flags are what stop invented testimonials and results. |
| `brand-board.md` | Graphics come out in neutral greys instead of your colours. They'll be well made and won't look like yours. |
| `style-guides/social.md` | Every post defaults to Instagram conventions and one repeated call to action, whether or not that fits. |
| `style-guides/ads.md` | If paid isn't marked active, campaign plans may include an ad budget the business never intended to spend. |
| the others | The matching content type falls back to general best practice rather than this business's conventions. Lower cost — fill them when that channel matters. |

**What a starter-pack default costs** — report these separately from placeholders, because the fix is different. A placeholder produces obviously generic output; a pack default produces *plausibly* generic output, which is harder to spot and therefore more expensive:

| Still a pack default | What it costs |
|---|---|
| `audience.md` | Content is written to a typical customer for the trade rather than yours. It will read fine and convert worse. |
| `brand-voice.md` voice pillars | It sounds like a competent business in your industry. It does not sound like you, and readers who know you will feel the difference before they can name it. |
| `style-guides/social.md` pillars | You'll post the right *shape* of content on the wrong topics for your actual customers. |
| `style-guides/ads.md` | The trade-typical answer may be wrong for you — if it says paid isn't active and it is, campaign plans will quietly omit it. |

Say plainly that confirming these takes a few minutes and is the highest-value thing they can do, and that it is done by saying "update my brand profile".

Also flag: a `brand-brief.md` at the workspace root **and** a filled profile. Both existing is fine — the profile wins — but say which one is being used, because two brand sources that disagree is a real failure mode.

## 2. Check what this installation can do

Probe each area live. Report **working / not connected / not applicable here**, then the consequence.

### Saving files
Confirm the workspace root resolved and is writable. Report which mode is in use (a folder on this computer, or Dropbox). In Dropbox mode, add that images can't sync through the connector — they stay on this computer and only the re-renderable source travels.
**If it fails:** nothing can be saved between sessions. This is the only finding that stops the product working at all — report it first and loudest.

### Making graphics
Probe in the order the render ladder actually uses:
1. Does Python resolve? Try `python3`, then `python`, then `py` — and **run each one, don't just check it exists**. On Windows `python3` is a Microsoft Store alias that passes an existence check and then fails when executed. Use the first whose `--version` actually prints a version.
2. Does `import PIL` succeed?
3. Is a usable font present? The renderer's cascade ends at a system font, then a bundled fallback.
4. Chromium — **only report this if it is present.** On Windows and macOS it is *not applicable*, not missing.

**If Python or Pillow is absent:** no finished images at all — copy only. This is the one hard dependency, and the fix is a one-line install (`pip install Pillow`), so say that rather than leaving it as a wall.

### Publishing
Search for a Blotato posting capability.
**If absent:** posts are still written and graded in full — you copy and paste each one yourself, with the caption, hashtags, and image path handed to you ready to paste. Nothing is lost except the scheduling step.

### Performance data
Search for a Facebook/Instagram insights capability.
**If absent:** the performance columns in the content calendar stay empty — never zero — so there's no measured record of what worked. Content still gets produced and graded; it just can't be scored against what actually performed. Note that paid-ad metrics are out of scope regardless.

### Reading your website
Search for a Firecrawl scrape capability.
**If absent:** setup falls back to a plain text fetch plus an interview. Brand colours and fonts can't be captured automatically — you'd supply those yourself, or accept neutral defaults.

### The menu
Probe for the widget renderer.
**If absent:** the menu appears as a plain numbered list instead of clickable cards. Every option still works and the numbers stay stable. This is a cosmetic difference, and it should be reported as one — not as a fault.

**Report only. Do not attempt to repair the menu here** — that belongs to the menu skill itself.

## 3. Write `.aimm/environment.md`

Create the `.aimm/` folder if it doesn't exist. Write what was found, using the same forgiving `key: value` shape as `aimm-config.md` so there is only ever one format to read:

```markdown
# Environment — written by doctor. Do not hand-edit.

> This records what was found the last time doctor ran. It goes stale.
> Any skill reading it should treat it as a hint and probe again before relying on it.

last_checked: 2026-08-16
workspace_root: C:\Users\jen\Documents\Acme Marketing
storage_mode: local

## Connectors present
[one per line: the capability, and the tool identifier that actually resolved]

## Not connected
[one per line, with the fallback now in use]

## Not applicable on this platform
[one per line — e.g. Chromium on Windows. Not faults.]

## Active fallbacks
[which degraded paths are currently in use, in plain words]
```

**Never write `aimm-config.md`.** That file belongs to the user. Doctor reads it and writes elsewhere.

Record the **real resolved tool identifiers** here — this is the one place they belong, because they were discovered rather than assumed.

## 4. Give the report

Plain language, shortest useful form. Lead with anything that actually blocks work, then anything that changes output quality, then anything cosmetic. If everything is working, say so in a line or two and don't manufacture concerns.

Shape:

```
Your brand setup
  [file] .......... [state]
     -> [what the gap costs, only when there is one]

What this installation can do
  Saving files .... working — a folder on this computer
  Making graphics . working
  Publishing ...... not connected
     -> you copy and paste each post yourself
  Performance ..... not connected
     -> the calendar's performance columns stay empty

What I'd do first
  [one or two concrete next actions, most valuable first — or nothing if there's nothing worth doing]
```

**"What I'd do first" is a recommendation, not an action.** Never carry it out in the same turn.

End by saying where the details were written, and that findings go stale — a connector can appear or vanish between sessions, so re-run this after anything changes.

## 5. Quality bar

- Every gap names a consequence. A status with no cost attached is not a finding.
- Nothing was fixed, installed, or configured.
- Every connector was found by capability; no literal `mcp__…` string was matched.
- "Not applicable here" was used where it belongs, and never dressed up as a failure.
- A fresh install with no profile produces a clear, calm report — not an error.
- Starter-pack defaults were reported as their own state, never folded into "filled". A profile that is 4/11 unconfirmed pack text and reported as complete is worse than no report at all.
- `.aimm/environment.md` was written and its path confirmed before being reported.
- Nothing in the user-facing report requires knowing what an MCP server is.

---
name: getting-started
description: >
  The help desk. Explains what to do first on a new install, what to do in the first week, and what to try when something isn't working or the output isn't good enough. Use when the user says "how do I start", "what do I do now", "I'm stuck", "this isn't working", "what should I do this week", "what should I post this week", "help", or asks what they've bought and what it can do. Also use after a failed or disappointing run, when the question is really "is this broken or am I doing it wrong?". Answers conversationally from bundled reference documents rather than dumping a manual, and hands off to doctor for anything that needs an actual diagnosis of the installation.
---

# Getting Started

The person reading this bought a marketing system and does not want to learn one. Answer the question they asked, in their words, and get them back to producing something.

**Never paste a whole document at them.** These references exist so you can answer a specific question well, not so a manual can be recited. Read the relevant one, answer in a few lines, and offer the next step.

---

## Workspace and file access — resolve this before any read or write

Every `Business/...`, `memory.md`, and other workspace path in this skill is relative to your workspace root. Resolve it **once** at the start of the run, then use the same method for every read and write that follows:

1. **The current project folder is the workspace root.** If a folder is open or mounted in this session, that folder is the root. This is the default and needs no configuration.
2. **`aimm-config.md` at that root can override it.** If it sets `workspace_root`, use that path instead. If it sets `storage_mode: dropbox`, read and write through the Dropbox tools at that path — found by capability, never by a literal `mcp__…` name.
3. **Nothing reachable.** Say so in one line and ask which folder to use.

A failed read is **not** proof a file is missing. Retry, or list the parent folder, before reporting anything absent — especially before saying a business profile doesn't exist.

**Before falling back to a lesser path,** check `.aimm/environment.md` for what `doctor` last found. Treat it as a hint, not proof — if it is stale or absent, probe and proceed. The live probe is always authoritative.

**Plugin-relative paths are the exception.** Paths beginning `assets/`, `scripts/`, `library/`, or `references/` live inside this skill's own folder in the installed plugin — *not* in the workspace root and *not* in Dropbox. Read those from the skill directory on every surface, mobile included, and never look for them through a connector.

**One business per workspace.** The active slug comes from `aimm-config.md` (`business:`), or the single folder under `Business/` that isn't `_template`.

---

## 1. Work out where they actually are

Check before answering — the right answer differs completely by stage, and guessing wastes their time.

| What you find | Where they are | What they need |
|---|---|---|
| No business profile under `Business/` | Brand new | Not this skill. Route to `business-setup` — there is nothing to explain until it knows the business. Say one line about what setup does, then go. |
| Profile exists, `examples/` is empty | Set up, never produced | "Make your first post." Section 2. |
| A few pieces in `examples/`, nothing scheduled | Producing, not publishing | The first-week plan. Section 3. |
| Something failed, or they say it's not working | Stuck | Section 4. |

**Don't ask which one they are.** Look.

## 2. The first post

The shortest honest route from a finished profile to something they can publish:

> Say **"make me a post"**. It'll ask what about — or say "you pick" and it'll suggest three angles from your own brand. You'll get the caption, the hashtags, the alt text, and a finished image saved into your folder.

That is `social-post-pack`. It grades the copy and rewrites it until it clears 8/10 before it renders anything, so the first thing they see is not a first draft.

**If they don't know what to post about**, that is a different problem and has its own skill: `content-coach` walks from "I don't know" to a scheduled post in one conversation. Route there rather than pushing them to pick a topic they don't have.

**If they want to see what's possible first**, `templates` shows twenty structures they can start from.

## 3. The first week

Read `references/first-week.md` and answer from it. It covers what to do on each of the first five days, why the order matters, what "good" looks like at the end of the week, and the two things most people do wrong in week one.

Give them the next day's step, not the whole week. A five-day plan delivered in one message is a five-day plan nobody starts.

## 4. When something isn't working

Read `references/troubleshooting.md` and answer from it. It covers: no image was produced, the writing sounds generic, publishing didn't happen, the menu looks like a plain list, performance numbers are empty, and the difference between "this is broken" and "this needs more from you".

**Run `doctor` first for anything that might be the installation** rather than guessing from symptoms. It probes live and reports what is actually connected. This skill explains; `doctor` diagnoses. Don't do its job from memory.

**The most common real cause is not a fault.** Generic-sounding output almost always means the business profile is thin, not that anything is broken — the fix is filling in `brand-voice.md`, not reinstalling. Say that plainly; it saves them an afternoon.

## 5. Quality bar

- Answer the question asked, in a few lines. Never paste a reference document wholesale.
- Look at the workspace before answering — a stage guess is usually wrong and always wastes time.
- Route to `doctor` for diagnosis, `business-setup` for a missing profile, `content-coach` for "I don't know what to post".
- Never claim something is broken without having checked. "I don't know yet, let me look" is a better answer than a confident wrong one.
- End with one concrete next action, not a summary of the options.

# AI Marketing Machine

Marketing content production for one small business, run inside your own Claude account, grounded in your own brand.

Twenty-eight skills covering social posts, carousels, blog posts, paid ads, campaigns, lead magnets, landing pages, SEO, and performance. Every one of them reads your voice, audience, and products from your own workspace at runtime — nothing is hardcoded to a brand, and nothing is stored on anyone else's server.

**With zero connectors configured it still works.** You get graded copy and a finished PNG saved to a folder on your computer. Publishing and performance measurement are optional upgrades, not requirements.

## Install

Add the plugin, then open a folder to work in. That folder is your workspace — no configuration needed.

Say `AI Marketing Machine` to open the menu, or run `business-setup` to build your brand profile from your website.

Want to know what's working before you start? Run `doctor`. It checks everything and tells you in plain English what each gap costs you.

**New here?** [docs/quick-start.md](docs/quick-start.md) walks the whole thing end to end in about half an hour. Once installed, say "how do I start" and the product walks you through it directly.

## Your workspace

```
MyBusiness/                    <- any folder; this is your workspace root
  aimm-config.md               <- optional settings (see below)
  memory.md                    <- running log of active work
  .aimm/environment.md         <- written by doctor; don't edit
  Business/
    my-business/
      context/                 <- your brand: the only hand-written folder
        brand-voice.md
        audience.md
        products.md
        brand-board.md
        style-guides/
      seo/                     <- everything below is generated
      social/
      visuals/
      examples/
```

`context/` is the one folder you ever edit by hand, and `business-setup` fills most of it for you. Everything else accumulates as you produce work.

## Settings

Settings are optional. **With no config file at all, everything uses its default** — the folder you have open is your workspace, storage is a plain local folder, and the one business profile under `Business/` is the active one.

To change any of that, copy `Business/_template/aimm-config.example.md` to your workspace root as `aimm-config.md` and edit it.

| Key | Default | What it does |
|---|---|---|
| `business` | the one folder under `Business/` that isn't `_template` | Which profile is active. |
| `workspace_root` | the folder containing `aimm-config.md` | Where your files live. Absolute path. |
| `storage_mode` | `local` | `local` or `dropbox`. Dropbox needs `workspace_root` set to a Dropbox path. |
| `business_name` | the slug, title-cased | How the business is named in finished content. |
| `time_zone` | your computer's | Used for scheduling and dating files. |
| `default_platform` | asks | Used when a request doesn't name one. |
| `default_ratio` | `4:5` | Image shape for social graphics. |
| `hashtag_cap` | each platform's own | Instagram's real cap is 5. |

How the file is read: a setting is the first line whose text before the first colon matches the key, case-insensitively. The value is everything after that colon, trimmed — so a Windows path with a drive letter is fine. An empty value means "use the default". Unknown keys are ignored rather than treated as errors. A missing file means all defaults.

The one hard error is `storage_mode: dropbox` with a blank `workspace_root`. The product will say so and ask rather than guessing a path.

## Optional connectors

None of these are required. Each has a defined fallback, so a missing service produces a lesser result and an honest sentence about it — never a dead end.

| Connector | What it adds | Without it |
|---|---|---|
| Firecrawl | Reads your website during setup to pull real copy, colours, fonts, and logo | Setup uses a plain text fetch plus the interview; you supply colours yourself or accept neutral defaults |
| Blotato | Schedules finished posts to Facebook and Instagram | You get a copy-paste block with caption, hashtags, and image path |
| Meta Graph API | Real reach and engagement written back into your content calendar | Performance columns stay empty — never zero |
| Dropbox | Cloud sync and phone access to your workspace | A plain local folder, which needs no account |
| A card renderer | The menu appears as clickable cards | The menu appears as a numbered list. Every option still works. |
| Chromium | A handful of layouts that need a real browser to render | The standard renderer handles everything else. Not available on Windows or Mac, and not needed there. |

**Rendering needs Python with [Pillow](https://pypi.org/project/Pillow/) installed.** That is the one hard dependency for finished graphics — everything else on this list is optional. It needs no network.

Not sure what you have? Ask for a check-up — `doctor` reports what's working, what isn't, and what each gap actually costs you.

## What it will not do

- Invent testimonials, results, or outcome numbers. Missing is stated as missing.
- Report performance figures it could not actually pull.
- Claim a file was saved without confirming the write first.
- Guess at your brand colours or voice when the profile is still a placeholder — it says so and uses neutral defaults.

## Skills

See [`skills/README.md`](skills/README.md) for the full list and how they fit together.

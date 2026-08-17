# [Business Name] — Brand Context

This folder holds everything specific to **[Business Name]** inside the AI Marketing Machine project. `memory.md` at the workspace root records active work across the whole workspace; this file and `memory.md` in this folder describe this one business. Claude Code reads both — root context first, then this folder's context layered on top — so business-specific facts don't need to be repeated in the root files, and root system facts don't need to be repeated here.

## Folder contents

- `context/` — brand voice, audience, products, brand board, and per-content-type style guides. Every skill reads this at runtime before producing anything for this business. This is the only folder that should ever contain hand-authored brand facts — everything else here is generated.
- `seo/` — SEO audits, keyword research, and content briefs (from `seo-audit` and `ai-search-blog-writer`).
- `social/` — the running content calendar (`content-calendar.md`) and social-specific archives (from `social-creative-designer`, `carousel-post-designer`, `campaign-plan`).
- `visuals/` — design briefs, image-generation JSON prompts, and exported PNGs (from `graphic-production-studio`).
- `examples/` — finished, approved copy across all content types — the calibration reference for this business's actual voice and structure, not just what the style guide says it should be.

## Working on this business

1. Read this file and `memory.md` in this folder first — business-specific facts, honesty flags, and open threads live here, not in the root files.
2. Read `context/brand-voice.md`, `context/audience.md`, and `context/products.md` before producing anything.
3. Check `seo/` and `examples/` for prior work before starting new research or drafts, so nothing gets duplicated or contradicted.
4. Save finished output to the matching typed folder, per the producing skill's own save instructions.

## Confidentiality

Each business folder is self-contained. If a workspace ever holds more than one, never pull one business's context or content into another's work.

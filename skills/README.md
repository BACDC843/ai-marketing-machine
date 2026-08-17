# Skills

Twenty-eight skills, each one folder with a `SKILL.md`. Every skill is brand-agnostic: it reads your business's voice, audience, products, and visual identity from `Business/[slug]/context/` at runtime and never hardcodes a brand value. That is what lets one library serve any business without forking it.

## Where to start

`menu` is the front door. Say "AI Marketing Machine" or "what can you do" and it shows the job list, then routes into the right specialist skill. You never need to remember a skill name.

If you have no business profile yet, run `business-setup` first — everything downstream reads the folder it builds.

## The skills

### Setup

| Skill | What it does |
|---|---|
| `business-setup` | Builds your `Business/[slug]/` folder from your website, existing documents, or a structured interview. Creates `context/` plus the `seo/`, `social/`, `visuals/`, and `examples/` output folders. |
| `brand-brief` | The fast version: six conversational questions producing a `brand-brief.md`. Use when you want to start posting today and fill in the full profile later. |

### Front doors

| Skill | What it does |
|---|---|
| `menu` | The router. Shows the job list and hands off. Does not produce content itself. |
| `content-coach` | For "help me post something" with no plan behind it — walks brand capture, ideas, draft, grade, and scheduling in one conversation. |
| `templates` | A gallery of twenty content structures — hook shapes, skeletons, render presets. Pick one and it hands the skeleton to the right production skill. |

### Writing

| Skill | What it does |
|---|---|
| `social-post-pack` | One request in, one publishable post out: copy, caption, hashtags, alt text, and an actual rendered PNG. The one-shot path. |
| `post-writer` | A single platform post from a topic. Auto-grades before returning. |
| `social-creative-designer` | Organic single- and multi-image posts — copy plus written visual direction, no rendering. |
| `carousel-post-designer` | Multi-slide carousels and LinkedIn document posts, slide by slide. |
| `ai-search-blog-writer` | Blog posts built for both traditional SEO and AI-search citation. |
| `lead-magnet` | Gated downloadable assets worth the email address they cost. |
| `landing-page-builder` | Section-by-section landing page copy, plus a self-contained coded page on request. |
| `ad-creative-brief` | The objective, audience, and angle, settled before any ad copy gets written. |
| `ad-creative-designer` | Meta ad creative built to current specs and character limits. |
| `weekly-content-plan` | A full week of posts in one batch, each graded to 8/10 or better and exported as a branded graphic. |

### Repurposing

| Skill | What it does |
|---|---|
| `repurposing-to-instagram` | An existing piece, rebuilt Instagram-native. |
| `repurposing-to-linkedin` | The same, for LinkedIn posts and document posts. |
| `repurposing-to-newsletter` | One source piece into one email newsletter issue. |

### Production

| Skill | What it does |
|---|---|
| `graphic-production-studio` | The shared visual engine. Turns approved copy into a design brief, an image-generation prompt, or an exported PNG, using your real brand tokens. The only skill that writes to `visuals/`. |

### Quality, planning, and measurement

| Skill | What it does |
|---|---|
| `post-grader` | Scores a post out of 10 for virality — hook strength at 50% — and returns ranked fixes. |
| `brand-review` | Checks any draft against your documented voice and flags deviations by severity, with before/after fixes. |
| `campaign-plan` | Coordinates multiple pieces toward one goal: objectives, channels, calendar, assets, metrics. |
| `seo-audit` | Technical, on-page, keyword, and content-gap audit, plus a dedicated local SEO and Google Business Profile section. |
| `performance-digest` | Pulls real engagement data, ranks content, and writes measured numbers back into your content calendar. |
| `website-portfolio-report` | One website URL into one compiled marketing portfolio document. |

### Publishing

| Skill | What it does |
|---|---|
| `post-scheduler` | Schedules an approved post through Blotato. Falls back to a copy-paste block when Blotato isn't connected. |

## How they fit together

1. **Setup** builds the context folder everything else depends on.
2. **Writing** skills read that context and produce copy plus visual direction.
3. **Production** turns approved copy into actual pixels.
4. **Quality, planning, and measurement** sit around the writing skills — they review, coordinate, and measure rather than originating content.
5. **Publishing** ships what has been approved.

## Conventions every skill follows

- **Workspace location is configuration.** Each skill resolves the workspace root once per run: the current project folder by default, or whatever `aimm-config.md` specifies. No skill assumes a fixed path.
- **Brand values are read, never written in.** A skill that hardcodes a colour, a tone, or a claim is a bug.
- **Templates hold structure only** — hook shapes, skeletons, render presets, CTA types.
- **Degrade, don't stop.** Every external dependency has a defined fallback. A missing connector produces a lesser result and an honest sentence about it, never a dead end.
- **Files are the deliverable.** Finished work is written into your workspace and the path is confirmed before it is reported. The conversation is not storage.
- **Never fabricate proof.** No invented testimonials, outcome numbers, or performance figures. Missing is stated as missing.

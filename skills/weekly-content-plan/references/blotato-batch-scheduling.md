# Scheduling a weekly batch via Blotato

This is the delta on top of `post-scheduler/SKILL.md` for scheduling a full week (up to 14 posts: 7 days x however many platforms the business actually uses) in one pass rather than one post at a time. Read `post-scheduler/SKILL.md` first for the base workflow (pre-publish check, error handling, fallback-to-file behavior) — this doc only covers what's different about doing it as a batch.

## Only when explicitly asked

Drafting a week of content and scheduling it are two different requests. Never auto-schedule after drafting — wait for the user to say "schedule these," "post these," or name specific days/times. If they only asked for the content, stop after saving it and rendering the artifact.

## Step 1: Match the business's platforms to Blotato accounts

Call `blotato_list_accounts` once, filter to the platforms the business's `style-guides/social.md` says they actually use (don't offer to schedule to a platform the business doesn't run). For Facebook, the `pageId` comes from that account's `subaccounts` array, matched by page name — if a business has ever rebranded or has multiple pages, confirm which page before scheduling anything, don't guess.

If a platform the business uses has zero connected accounts, don't block the whole batch — schedule what you can, and report the gap plainly (matches `post-scheduler`'s existing fallback behavior, just applied per-platform instead of per-post).

## Step 2: Upload every graphic once, reuse the URL

`blotato_create_post`'s `mediaUrls` needs a public URL, not a local path. For each day's graphic (one PNG can serve both the Instagram and Facebook version of that day, since they share the same visual):

1. `blotato_create_presigned_upload_url({filename: "..."})` → returns `presignedUrl` (for uploading) and `publicUrl` (for use in `create_post`).
2. Upload the actual bytes with an HTTP PUT of the raw file to `presignedUrl` — not JSON, not multipart, the raw bytes (`curl -X PUT "<presignedUrl>" --data-binary "@<local_png_path>"`).
3. Confirm the PUT returned 200 before using the `publicUrl` — don't assume success.
4. Reuse the same `publicUrl` across every platform's post for that day rather than re-uploading per platform.

Batch all 7 uploads before batching the `create_post` calls — it's more parallelizable and keeps the two concerns (getting media hosted vs. actually scheduling) separate, which makes partial failures easier to diagnose.

## Step 3: The Instagram hashtag cap is real and lower than most style guides say

**Confirmed against the live API (2026-08-06): Blotato enforces a hard 5-hashtag cap on Instagram posts and rejects anything over that with `"Instagram allows a maximum of 5 hashtags per post."`** This is true even when the business's own `style-guides/social.md` documents a higher range — a range like 8-15 is real for organic Instagram itself, just not for what Blotato's API will accept.

Don't discover this by trial and error every time — for any Instagram post going through Blotato, always trim to 5 hashtags before the first `create_post` attempt: the business's 2-3 mandatory brand hashtags, plus the 2-3 highest-relevance category/local tags for that specific post's topic. Save both the full draft hashtag set (for the business's own record of what their real style guide calls for) and the trimmed set actually sent, and note in the saved post file which one shipped — see Section 7 of `SKILL.md`.

If a another business's style guide also calls for more than 5 and this cap is ever lifted or turns out to be account-specific rather than a Blotato-wide limit, update this note rather than assuming the cap is permanent — it hasn't been tested against every account tier.

## Step 4: Schedule, then write real IDs back into the project files

For each post, call `create_post` with `scheduledTime` (an explicit ISO 8601 timestamp per day, not `useNextFreeSlot`, since a weekly batch needs a chosen cadence rather than whatever Blotato's queue happens to pick next) and the platform-specific required fields (`pageId` for Facebook, `mediaUrls` for Instagram).

After every call resolves (success or failure), write the result back into both:
1. The per-post file saved in `Business/[slug]/social/` — add the returned `postSubmissionId` and confirmed `scheduledTime`, and if the actual hashtags sent differ from the drafted set (see Step 3), record both.
2. `Business/[slug]/social/content-calendar.md` — update that row's Status column from "Drafted"/"Scheduled for review" to "Scheduled via Blotato for [timestamp]" with the IDs.

A post that was scheduled but never recorded as such is indistinguishable from one that failed, the next time anyone reads these files — always close the loop in writing, not just in the chat response.

## Step 5: Say the quiet part about cadence

If the user asks to schedule the full week across every channel, that's very likely more volume than the business's own documented posting cadence (check `style-guides/social.md`'s posting-frequency line, e.g. "3-5 IG/week, 1-2 FB/week"). Scheduling 7 posts on a channel the business says should get 1-2/week isn't wrong to execute if that's what was asked, but it's worth surfacing plainly in the final report — one or two sentences, not a blocking question — so the user can thin it out in Blotato's own scheduler (`https://my.blotato.com/scheduler`) before anything actually goes live, rather than finding out after the fact that a week's worth of posts published back-to-back.

## Never silently launder an unresolved flag through scheduling

If a post carries an open flag from drafting (an unverified regulatory/legal claim, a fictional-but-realistic scenario, an AI-generated photo — see `SKILL.md` Section 10), scheduling it doesn't resolve that flag. Repeat it in the scheduling confirmation, not just the original draft file, so it doesn't get lost between "drafted" and "live."

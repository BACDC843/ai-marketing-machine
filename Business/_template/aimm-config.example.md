# AI Marketing Machine — Settings

Copy this file to the top of your workspace folder, rename it to
`aimm-config.md`, and edit the values.

Edit the value after each colon. Leave a value blank to use the default.
Lines starting with `>` are notes and are ignored.
Delete this whole file and everything falls back to its default — that is a
supported setup, not a broken one.

## Workspace

business: my-business
> Which folder under `Business/` is active. Must match the folder name exactly.
> Leave blank if you only have one — it will be found automatically.

workspace_root:
> Where your marketing files live. Leave blank to use the folder this file sits
> in — that is the normal setup. Set it only if your files live somewhere else,
> for example: C:\Users\jen\Documents\Acme Marketing

storage_mode: local
> `local`   — files on this computer. The default, and needs no account.
> `dropbox` — files live in Dropbox and are read and written through the
>             Dropbox connector. If you use this, `workspace_root` must be the
>             full Dropbox path starting with a slash, e.g. /Acme Marketing

## Your business

business_name: My Business
> How the business is named in finished content. Defaults to the folder name,
> title-cased.

time_zone: America/New_York
> Used for scheduling and for dating saved files. Defaults to this computer's
> time zone.

## Defaults — all optional

default_platform: Instagram
> Used when a request doesn't name a platform.

default_ratio: 4:5
> Image shape for social graphics. 4:5, 1:1, 9:16, or 1.91:1.

hashtag_cap:
> Leave blank to use each platform's own limit. Instagram's real cap is 5.

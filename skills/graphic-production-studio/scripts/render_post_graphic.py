#!/usr/bin/env python3
"""
render_post_graphic.py — Pillow-based social graphic renderer.

The dependency-light export path for social-post-pack. No Chromium, no
Playwright, no network. If Pillow imports, this works.

Usage:
    python3 render_post_graphic.py spec.json out.png

Spec (JSON). Only `headline` is required; everything else has a default.

{
  "layout":       "editorial" | "photo-overlay" | "quote",
  "width":        1080,
  "height":       1350,
  "bg":           "#1B1B1B",
  "accent":       "#C9A227",
  "text_color":   "#FFFFFF",
  "muted_color":  "#B8B8B8",
  "eyebrow":      "YOUR BUSINESS",
  "headline":     "The quote is not the price.",
  "subhead":      "Here is what changes between the two.",
  "footer":       "yourbusiness.com",
  "photo_path":   "/abs/path/photo.jpg",
  "logo_path":    "/abs/path/logo.png",
  "font_regular": "/abs/path/Font-Regular.ttf",
  "font_bold":    "/abs/path/Font-Bold.ttf",
  "scrim":        0.62
}

Exit codes: 0 ok, 2 bad spec, 3 Pillow missing.
"""

import json
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    sys.stderr.write(
        "Pillow is not installed. Run: pip install Pillow --break-system-packages\n"
    )
    sys.exit(3)


# --------------------------------------------------------------------------
# Fonts
# --------------------------------------------------------------------------

FONT_CANDIDATES_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]

FONT_CANDIDATES_REGULAR = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "C:/Windows/Fonts/arial.ttf",
]


def _matplotlib_fonts():
    """matplotlib ships DejaVu; use it as a last-resort font source."""
    try:
        import matplotlib
        base = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
        return (
            os.path.join(base, "DejaVuSans-Bold.ttf"),
            os.path.join(base, "DejaVuSans.ttf"),
        )
    except Exception:
        return (None, None)


def resolve_font(explicit, candidates, mpl_index):
    if explicit and os.path.exists(explicit):
        return explicit
    for path in candidates:
        if os.path.exists(path):
            return path
    mpl = _matplotlib_fonts()[mpl_index]
    if mpl and os.path.exists(mpl):
        return mpl
    return None


def load_font(path, size):
    if path:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


# --------------------------------------------------------------------------
# Text helpers
# --------------------------------------------------------------------------

def text_size(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def wrap(draw, text, font, max_width):
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if text_size(draw, trial, font)[0] <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_headline(draw, text, font_path, max_width, max_height, start, minimum=34):
    """Shrink until the wrapped headline fits its box. Never overflow."""
    size = start
    while size >= minimum:
        font = load_font(font_path, size)
        lines = wrap(draw, text, font, max_width)
        line_h = int(size * 1.20)
        if len(lines) * line_h <= max_height:
            return font, lines, line_h
        size -= 3
    font = load_font(font_path, minimum)
    return font, wrap(draw, text, font, max_width), int(minimum * 1.20)


def draw_lines(draw, lines, font, x, y, line_h, fill):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_h
    return y


def trim_alpha(img):
    """Crop transparent padding so the logo sizes to its actual ink."""
    box = img.getbbox()
    return img.crop(box) if box else img


def paste_logo(canvas, logo_path, x, y, max_w, max_h):
    """Paste a logo anchored top-left in the given box. Returns (w, h) drawn."""
    if not logo_path or not os.path.exists(logo_path):
        return (0, 0)
    try:
        logo = trim_alpha(Image.open(logo_path).convert("RGBA"))
    except Exception:
        return (0, 0)
    ratio = min(max_w / logo.width, max_h / logo.height)
    logo = logo.resize((max(1, int(logo.width * ratio)), max(1, int(logo.height * ratio))), Image.LANCZOS)
    canvas.paste(logo, (int(x), int(y)), logo)
    return (logo.width, logo.height)


def draw_logo_panel(canvas, spec, logo_path, right, bottom, max_logo_h, accent):
    """
    Place a logo inside a light panel, bottom-right anchored at (right, bottom).

    Many brand systems require a light backing panel when a dark-ink logo sits on
    a dark background, since recoloring the mark is usually prohibited. Returns
    the panel's (left, top) or None if nothing was drawn.
    """
    if not logo_path or not os.path.exists(logo_path):
        return None
    try:
        logo = trim_alpha(Image.open(logo_path).convert("RGBA"))
    except Exception:
        return None

    ratio = max_logo_h / logo.height
    lw, lh = max(1, int(logo.width * ratio)), max(1, int(logo.height * ratio))
    logo = logo.resize((lw, lh), Image.LANCZOS)

    pad = int(spec.get("logo_panel_padding", 26))
    pw, ph = lw + pad * 2, lh + pad * 2
    left, top = int(right - pw), int(bottom - ph)

    panel_rgb = Image.new("RGB", (1, 1), spec.get("logo_panel_bg", "#FAFAF8")).getpixel((0, 0))
    ar, ag, ab = Image.new("RGB", (1, 1), accent).getpixel((0, 0))

    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle(
        [left, top, left + pw, top + ph],
        radius=int(spec.get("logo_panel_radius", 4)),
        fill=panel_rgb + (int(255 * float(spec.get("logo_panel_opacity", 0.96))),),
        outline=(ar, ag, ab, int(255 * float(spec.get("logo_panel_border_opacity", 0.35)))),
        width=1,
    )
    merged = Image.alpha_composite(canvas.convert("RGBA"), overlay)
    merged.paste(logo, (left + pad, top + pad), logo)
    canvas.paste(merged.convert("RGB"), (0, 0))
    return (left, top)


def cover(img, width, height):
    """Resize + center-crop to exactly fill width x height."""
    ratio = max(width / img.width, height / img.height)
    img = img.resize((max(1, int(img.width * ratio)), max(1, int(img.height * ratio))), Image.LANCZOS)
    left = (img.width - width) // 2
    top = (img.height - height) // 2
    return img.crop((left, top, left + width, top + height))


# --------------------------------------------------------------------------
# Layouts
# --------------------------------------------------------------------------

def render(spec, out_path):
    W = int(spec.get("width", 1080))
    H = int(spec.get("height", 1350))
    layout = spec.get("layout", "editorial")

    bg = spec.get("bg", "#1B1B1B")
    accent = spec.get("accent", "#C9A227")
    text_color = spec.get("text_color", "#FFFFFF")
    muted = spec.get("muted_color", spec.get("muted", "#B8B8B8"))

    bold_path = resolve_font(spec.get("font_bold"), FONT_CANDIDATES_BOLD, 0)
    reg_path = resolve_font(spec.get("font_regular"), FONT_CANDIDATES_REGULAR, 1)

    photo_path = spec.get("photo_path")
    has_photo = bool(photo_path and os.path.exists(photo_path))

    if layout == "photo-overlay" and has_photo:
        canvas = cover(Image.open(photo_path).convert("RGB"), W, H)
        scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(scrim)
        strength = float(spec.get("scrim", 0.62))
        for i in range(H):
            # transparent at top, darkest at bottom
            alpha = int(255 * strength * (i / H) ** 1.35)
            sd.line([(0, i), (W, i)], fill=(0, 0, 0, alpha))
        canvas = Image.alpha_composite(canvas.convert("RGBA"), scrim).convert("RGB")
    else:
        canvas = Image.new("RGB", (W, H), bg)
        if has_photo:
            # editorial with a photo: photo occupies the top 48%
            band_h = int(H * 0.48)
            canvas.paste(cover(Image.open(photo_path).convert("RGB"), W, band_h), (0, 0))

    draw = ImageDraw.Draw(canvas)
    margin = int(W * 0.085)
    content_w = W - (margin * 2)

    # Optional inset hairline border (brand systems often specify one).
    if spec.get("border"):
        inset = int(spec.get("border_inset", W * 0.026))
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        r, g, b = Image.new("RGB", (1, 1), accent).getpixel((0, 0))
        alpha = int(255 * float(spec.get("border_opacity", 0.7)))
        od.rectangle([inset, inset, W - inset - 1, H - inset - 1],
                     outline=(r, g, b, alpha), width=int(spec.get("border_width", 2)))
        canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
        draw = ImageDraw.Draw(canvas)

    eyebrow = (spec.get("eyebrow") or "").strip()
    headline = (spec.get("headline") or "").strip()
    subhead = (spec.get("subhead") or "").strip()
    footer = (spec.get("footer") or "").strip()

    if not headline:
        sys.stderr.write("spec.headline is required\n")
        sys.exit(2)

    # ---- bottom-anchored stack (photo-overlay) or top-anchored (editorial)
    bottom_anchored = layout == "photo-overlay" and has_photo

    eyebrow_font = load_font(bold_path, int(W * 0.026))
    sub_font = load_font(reg_path, int(W * 0.036))
    foot_font = load_font(reg_path, int(W * 0.026))

    headline_box_h = int(H * (0.34 if layout == "quote" else 0.30))
    headline_font, headline_lines, line_h = fit_headline(
        draw, headline, bold_path, content_w, headline_box_h, int(W * 0.072)
    )

    sub_lines = wrap(draw, subhead, sub_font, content_w) if subhead else []
    sub_line_h = int(W * 0.036 * 1.45)

    block_h = 0
    if eyebrow:
        block_h += int(W * 0.026) + int(H * 0.028)
    block_h += len(headline_lines) * line_h
    if sub_lines:
        block_h += int(H * 0.022) + len(sub_lines) * sub_line_h

    if bottom_anchored:
        y = H - margin - int(H * 0.055) - block_h
    elif has_photo:
        y = int(H * 0.48) + int(H * 0.075)
    else:
        # Optically center the block in the space actually available to it —
        # above the footer rule, and above the logo panel when one is present.
        # Ignoring the panel is what leaves a void between copy and mark.
        top = int(margin * 1.4)
        reserved = int(H * 0.035)
        if spec.get("logo_path") and spec.get("logo_panel"):
            panel_h = int(spec.get("logo_height", H * 0.062)) + int(spec.get("logo_panel_padding", 26)) * 2
            reserved += panel_h + int(H * 0.044)
        avail = (H - margin - reserved) - top
        y = top + max(0, int((avail - block_h) * 0.5))

    if eyebrow:
        draw.text((margin, y), eyebrow.upper(), font=eyebrow_font, fill=accent)
        y += int(W * 0.026) + int(H * 0.028)

    if layout == "quote":
        rule_h = len(headline_lines) * line_h
        draw.rectangle([margin - int(W * 0.028), y, margin - int(W * 0.028) + 6, y + rule_h], fill=accent)

    y = draw_lines(draw, headline_lines, headline_font, margin, y, line_h, text_color)

    if sub_lines:
        y += int(H * 0.022)
        y = draw_lines(draw, sub_lines, sub_font, margin, y, sub_line_h, muted)

    # ---- logo panel (sits above the footer rule, right-aligned)
    foot_y = H - margin
    rule_y = foot_y - int(H * 0.035)
    logo_path = spec.get("logo_path")

    if logo_path and spec.get("logo_panel"):
        draw_logo_panel(
            canvas, spec, logo_path,
            right=W - margin,
            bottom=rule_y - int(H * 0.022),
            max_logo_h=int(spec.get("logo_height", H * 0.062)),
            accent=accent,
        )
        draw = ImageDraw.Draw(canvas)

    # ---- footer rule + wordmark
    draw.line([(margin, rule_y), (W - margin, rule_y)], fill=accent, width=2)
    if footer:
        fh = text_size(draw, footer, foot_font)[1]
        draw.text((margin, foot_y - fh - int(H * 0.004)), footer, font=foot_font, fill=muted)

    # bare logo (no panel) tucks into the footer line, right-aligned
    if logo_path and not spec.get("logo_panel"):
        logo_h = int(spec.get("logo_height", H * 0.032))
        lw, lh = paste_logo(canvas, logo_path, 0, 0, int(W * 0.16), logo_h)
        if lw:
            paste_logo(canvas, logo_path, W - margin - lw,
                       foot_y - lh - int(H * 0.004), int(W * 0.16), logo_h)

    canvas.save(out_path, "PNG", optimize=True)
    return out_path


def main():
    if len(sys.argv) < 3:
        sys.stderr.write("usage: render_post_graphic.py spec.json out.png\n")
        sys.exit(2)
    with open(sys.argv[1], "r", encoding="utf-8") as fh:
        spec = json.load(fh)
    path = render(spec, sys.argv[2])
    print(path)


if __name__ == "__main__":
    main()

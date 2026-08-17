"""
Bake one editorial social graphic (headline/body/CTA baked onto a photo, or
onto a solid brand background when no photo exists) into a real, ready-to-post
PNG using Pillow. Reads every colour, font, and wordmark from the business's
own brand-board tokens rather than a hardcoded palette, so one script serves
any brand.

WHY THIS SCRIPT EXISTS INSTEAD OF AN HTML/PLAYWRIGHT EXPORT:
This project's sandbox blocks the Chromium binary download and has no system
Chromium, so a Playwright HTML-screenshot pipeline silently fails here unless
Full internet access is on. Pillow has no such dependency, so it's the
reliable default for this environment. If graphic-production-studio's Mode F
(Playwright) is confirmed working in a given session, that's a fine
alternative -- this script is the one to reach for when it isn't, which is
the common case for this project.

REQUIREMENTS: pip install pillow

USAGE:
    python flatten_editorial_post.py post_config.json

post_config.json shape -- see the CONFIG_EXAMPLE dict at the bottom of this
file for a fully worked example. Every color is a hex string; the script
converts it. All brand values (colors, fonts) should come from the business's
real Business/[slug]/context/brand-board.md -- don't invent palette values
here, pass them in from that file.

{
  "canvas": {"width": 1080, "height": 1350},
  "layout": "full-bleed" | "split" | "cta" | "card",
  "source_photo": "path/to/photo.png or null for layout=card",
  "output_path": "path/to/output.png",
  "brand": {
    "primary_dark": "#0B1F2E",
    "accent": "#C99A4A",
    "accent_soft": "#D8B36C",
    "light_bg": "#FAFAF8",
    "panel_bg": "#EFE9DE",
    "ink": "#182433",
    "logo_wordmark": "YOUR BUSINESS"
  },
  "copy": {
    "headline": "6 weeks before anyone starts work.",
    "body": "That's often the real timeline once approvals\nand scheduling are accounted for.",
    "cta": null
  },
  "photo_disclosure": "ai-generated" | "real" | null,
  "slide_counter": null
}

If "photo_disclosure" is "ai-generated", the script stamps a small, honest
"AI-generated image" tag in the corner -- never ship a synthetic photo as if
it were a real project photo without saying so.
"""

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i : i + 2], 16) for i in (0, 2, 4))


def font(path_options, size):
    for p in path_options:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


# System-native fallback stacks -- covers Windows (this project's actual
# environment), and Mac/Linux in case the skill ever runs somewhere else.
SERIF_PATHS = [
    r"C:\Windows\Fonts\georgia.ttf",
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]
SANS_PATHS = [
    r"C:\Windows\Fonts\arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
SANS_BOLD_PATHS = [
    r"C:\Windows\Fonts\arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def cover_resize(img, w, h):
    """Resize+crop like CSS object-fit: cover."""
    src_ratio = img.width / img.height
    tgt_ratio = w / h
    if src_ratio > tgt_ratio:
        new_h, new_w = h, int(h * src_ratio)
    else:
        new_w, new_h = w, int(w / src_ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left, top = (new_w - w) // 2, (new_h - h) // 2
    return img.crop((left, top, left + w, top + h))


def gradient_overlay(size, direction, color, max_alpha=225, stop=0.68):
    w, h = size
    grad = Image.new("L", (1, h), 0)
    for y in range(h):
        t = 1 - min(y / (h * stop), 1)
        if direction == "top":
            t = 1 - t
        grad.putpixel((0, y), int(max_alpha * t))
    grad = grad.resize((w, h))
    overlay = Image.new("RGBA", size, color + (0,))
    overlay.putalpha(grad)
    return overlay


def full_vignette(size, color, max_alpha=210):
    w, h = size
    overlay = Image.new("L", size, 0)
    cx, cy = w / 2, h / 2
    maxd = (cx**2 + cy**2) ** 0.5
    px = overlay.load()
    for y in range(h):
        for x in range(w):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            px[x, y] = int(max_alpha * (0.35 + 0.65 * (d / maxd)))
    out = Image.new("RGBA", size, color + (0,))
    out.putalpha(overlay)
    return out


def draw_multiline(draw, xy, lines, fnt, fill, line_spacing=1.15):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * line_spacing)
    return y


def draw_disclosure_tag(draw, canvas_w, text, bg, fg):
    tag_font = font(SANS_PATHS, 18)
    w = draw.textlength(text, font=tag_font)
    pad = 10
    draw.rectangle([16, 16, 16 + w + pad * 2, 16 + 30], fill=bg + (210,))
    draw.text((16 + pad, 22), text, font=tag_font, fill=fg + (255,))


def draw_slide_counter(draw, canvas_w, label, bg, fg):
    cf = font(SANS_BOLD_PATHS, 22)
    w = draw.textlength(label, font=cf)
    draw.rectangle([canvas_w - w - 60, 30, canvas_w - 30, 68], fill=bg + (200,))
    draw.text((canvas_w - w - 45, 38), label, font=cf, fill=fg + (255,))


def flatten(config):
    canvas_w = config["canvas"]["width"]
    canvas_h = config["canvas"]["height"]
    layout = config["layout"]
    brand = {k: hex_to_rgb(v) if isinstance(v, str) and v.startswith("#") else v for k, v in config["brand"].items()}
    copy = config["copy"]
    output_path = Path(config["output_path"])
    output_path.parent.mkdir(parents=True, exist_ok=True)

    dark = brand["primary_dark"]
    accent = brand["accent"]
    accent_soft = brand.get("accent_soft", accent)
    light_bg = brand.get("light_bg", (250, 250, 248))
    panel_bg = brand.get("panel_bg", light_bg)
    ink = brand.get("ink", (24, 36, 51))

    canvas = Image.new("RGBA", (canvas_w, canvas_h))
    source_photo = config.get("source_photo")

    if layout == "card":
        # No photo: pure typographic card on a brand-color background.
        # Use this when there's no real project photo and the business's
        # brand-board.md / visual asset library makes a text-forward
        # editorial card more natural than a synthesized photo.
        canvas.paste(Image.new("RGBA", (canvas_w, canvas_h), dark + (255,)), (0, 0))
        draw = ImageDraw.Draw(canvas)
        h_font = font(SERIF_PATHS, 54)
        b_font = font(SANS_PATHS, 30)
        pad = 80
        headline_lines = copy["headline"].split("\n")
        body_lines = (copy.get("body") or "").split("\n") if copy.get("body") else []
        total_h = len(headline_lines) * int(h_font.size * 1.1) + (
            (24 + len(body_lines) * int(b_font.size * 1.4)) if body_lines else 0
        )
        y = (canvas_h - total_h) // 2
        y = draw_multiline(draw, (pad, y), headline_lines, h_font, light_bg + (255,), 1.1)
        if body_lines:
            y += 24
            draw.rectangle([pad, y, pad + 90, y + 3], fill=accent + (255,))
            y += 24
            draw_multiline(draw, (pad, y), body_lines, b_font, light_bg + (225,), 1.4)
        if copy.get("cta"):
            cta_font = font(SANS_BOLD_PATHS, 24)
            draw.text((pad, canvas_h - 100), copy["cta"], font=cta_font, fill=accent_soft + (255,))

    elif layout == "split":
        panel_w = int(canvas_w * 0.45)
        photo_w = canvas_w - panel_w
        photo = cover_resize(Image.open(source_photo).convert("RGBA"), photo_w, canvas_h)
        canvas.paste(photo, (panel_w, 0))
        draw = ImageDraw.Draw(canvas)
        draw.rectangle([0, 0, panel_w, canvas_h], fill=panel_bg + (255,))
        h_font = font(SERIF_PATHS, 46)
        b_font = font(SANS_PATHS, 27)
        pad = 44
        headline_lines = copy["headline"].split("\n")
        body_lines = (copy.get("body") or "").split("\n") if copy.get("body") else []
        y = canvas_h // 2 - 150
        y = draw_multiline(draw, (pad, y), headline_lines, h_font, ink + (255,), 1.12)
        if body_lines:
            y += 16
            draw.rectangle([pad, y, pad + 110, y + 4], fill=accent + (255,))
            y += 28
            draw_multiline(draw, (pad, y), body_lines, b_font, ink + (255,), 1.4)

    elif layout == "cta":
        img = cover_resize(Image.open(source_photo).convert("RGBA"), canvas_w, canvas_h)
        canvas.paste(img, (0, 0))
        overlay = full_vignette((canvas_w, canvas_h), dark)
        canvas = Image.alpha_composite(canvas, overlay)
        draw = ImageDraw.Draw(canvas)
        h_font = font(SERIF_PATHS, 50)
        c_font = font(SANS_BOLD_PATHS, 25)
        lines = copy["headline"].split("\n")
        total_h = len(lines) * int(h_font.size * 1.15)
        y = canvas_h // 2 - total_h // 2 - 50
        for line in lines:
            w = draw.textlength(line, font=h_font)
            draw.text(((canvas_w - w) / 2, y), line, font=h_font, fill=light_bg + (255,))
            y += int(h_font.size * 1.15)
        if copy.get("cta"):
            y += 34
            w = draw.textlength(copy["cta"], font=c_font)
            draw.text(((canvas_w - w) / 2, y), copy["cta"], font=c_font, fill=accent_soft + (255,))
        if brand.get("logo_wordmark"):
            logo_font = font(SERIF_PATHS, 20)
            lw = draw.textlength(brand["logo_wordmark"], font=logo_font)
            draw.text(((canvas_w - lw) / 2, canvas_h - 55), brand["logo_wordmark"], font=logo_font, fill=light_bg + (220,))

    else:  # full-bleed (default)
        img = cover_resize(Image.open(source_photo).convert("RGBA"), canvas_w, canvas_h)
        canvas.paste(img, (0, 0))
        overlay = gradient_overlay((canvas_w, canvas_h), config.get("overlay_direction", "bottom"), dark)
        canvas = Image.alpha_composite(canvas, overlay)
        draw = ImageDraw.Draw(canvas)
        h_font = font(SERIF_PATHS, 52)
        b_font = font(SANS_PATHS, 29)
        pad = 64
        headline_lines = copy["headline"].split("\n")
        body_lines = (copy.get("body") or "").split("\n") if copy.get("body") else []
        if config.get("text_pos") == "top":
            y = 100
        else:
            total_h = len(headline_lines) * int(h_font.size * 1.12) + (
                (22 + len(body_lines) * int(b_font.size * 1.4)) if body_lines else 0
            )
            y = canvas_h - total_h - 110
        y = draw_multiline(draw, (pad, y), headline_lines, h_font, light_bg + (255,), 1.12)
        if body_lines:
            y += 18
            draw_multiline(draw, (pad, y), body_lines, b_font, light_bg + (235,), 1.4)

    draw = ImageDraw.Draw(canvas)
    if config.get("photo_disclosure") == "ai-generated":
        draw_disclosure_tag(draw, canvas_w, "AI-generated image", dark, light_bg)
    if config.get("slide_counter"):
        draw_slide_counter(draw, canvas_w, config["slide_counter"], dark, accent)

    canvas.convert("RGB").save(output_path, "PNG")
    print(f"Saved {output_path}")


CONFIG_EXAMPLE = {
    "canvas": {"width": 1080, "height": 1350},
    "layout": "card",
    "source_photo": None,
    "output_path": "example-output.png",
    "brand": {
        "primary_dark": "#0B1F2E",
        "accent": "#C99A4A",
        "accent_soft": "#D8B36C",
        "light_bg": "#FAFAF8",
        "panel_bg": "#EFE9DE",
        "ink": "#182433",
        "logo_wordmark": "YOUR BUSINESS",
    },
    "copy": {
        "headline": "6 weeks before anyone starts work.",
        "body": "That's often the real timeline once approvals\nand scheduling are accounted for.",
        "cta": None,
    },
    "photo_disclosure": None,
    "slide_counter": None,
}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python flatten_editorial_post.py post_config.json")
        print("Writing an example config to example_post_config.json instead.")
        Path("example_post_config.json").write_text(json.dumps(CONFIG_EXAMPLE, indent=2), encoding="utf-8")
        sys.exit(0)
    config = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    flatten(config)

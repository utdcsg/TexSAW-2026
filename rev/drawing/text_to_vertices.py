#!/usr/bin/env python3
"""
text_to_vertices.py
====================
Converts a string of text into a C++ Vertex array for the Nintendo Switch
OpenGL homebrew template, and can automatically patch main.cpp in-place.

Usage
-----
    # Print vertex snippet to stdout
    python text_to_vertices.py "HELLO"

    # Patch main.cpp directly (idempotent — safe to run repeatedly)
    python text_to_vertices.py "HELLO" --patch main.cpp

    # All options
    python text_to_vertices.py "HELLO WORLD" \\
        --patch   main.cpp          \\
        --font    /path/to/font.ttf \\
        --font-size 64              \\
        --color   1.0 0.8 0.2       \\
        --bg-color 0.05 0.05 0.1    \\
        --scale   0.85              \\
        --y-offset 0.05             \\
        --output  snippet.cpp       \\
        --backup                    # keep main.cpp.bak before patching

Sentinel comments used in main.cpp
-----------------------------------
The patcher looks for these exact marker lines and rewrites the content
between them.  They are already present in the provided main.cpp template.

  Vertices block  (inside sceneInit):
    // <<<TEXT_VERTICES_BEGIN>>>
    ... generated vertex array ...
    // <<<TEXT_VERTICES_END>>>

  Draw-count line (inside sceneRender / sceneInit):
    glDrawArrays(GL_TRIANGLES, 0, /*<<<VERTEX_COUNT>>>*/ 3 /*<<<VERTEX_COUNT_END>>>*/);

  Background colour line (inside sceneRender):
    glClearColor(/*<<<BG_COLOR>>>*/ 0.2f, 0.3f, 0.3f, 1.0f /*<<<BG_COLOR_END>>>*/);

Requirements
------------
    pip install Pillow      # needed only when --font is used
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

# ── Sentinel strings ────────────────────────────────────────────────────────
VERTS_BEGIN   = "// <<<TEXT_VERTICES_BEGIN>>>"
VERTS_END     = "// <<<TEXT_VERTICES_END>>>"
COUNT_RE      = re.compile(
    r'(glDrawArrays\s*\(\s*GL_TRIANGLES\s*,\s*0\s*,\s*)'
    r'/\*<<<VERTEX_COUNT>>>\*/\s*\d+\s*/\*<<<VERTEX_COUNT_END>>>\*/'
    r'(\s*\))'
)
COUNT_REPL    = r'\g<1>/*<<<VERTEX_COUNT>>>*/ {count} /*<<<VERTEX_COUNT_END>>>*/\g<2>'

BGCOL_RE      = re.compile(
    r'(glClearColor\s*\()'
    r'\s*/\*<<<BG_COLOR>>>\*/.*?/\*<<<BG_COLOR_END>>>\*/'
    r'(\s*\))'
)
BGCOL_REPL    = r'\g<1>/*<<<BG_COLOR>>>*/ {r}f, {g}f, {b}f, 1.0f /*<<<BG_COLOR_END>>>*/\g<2>'

# ---------------------------------------------------------------------------
# Built-in 8×8 bitmap font (ASCII 32–126, public domain)
# ---------------------------------------------------------------------------
FONT8X8 = {
    ' ': [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
    '!': [0x18,0x3C,0x3C,0x18,0x18,0x00,0x18,0x00],
    '"': [0x36,0x36,0x00,0x00,0x00,0x00,0x00,0x00],
    '#': [0x36,0x36,0x7F,0x36,0x7F,0x36,0x36,0x00],
    '$': [0x0C,0x3E,0x03,0x1E,0x30,0x1F,0x0C,0x00],
    '%': [0x00,0x63,0x33,0x18,0x0C,0x66,0x63,0x00],
    '&': [0x1C,0x36,0x1C,0x6E,0x3B,0x33,0x6E,0x00],
    "'": [0x06,0x06,0x03,0x00,0x00,0x00,0x00,0x00],
    '(': [0x18,0x0C,0x06,0x06,0x06,0x0C,0x18,0x00],
    ')': [0x06,0x0C,0x18,0x18,0x18,0x0C,0x06,0x00],
    '*': [0x00,0x66,0x3C,0xFF,0x3C,0x66,0x00,0x00],
    '+': [0x00,0x0C,0x0C,0x3F,0x0C,0x0C,0x00,0x00],
    ',': [0x00,0x00,0x00,0x00,0x00,0x0C,0x0C,0x06],
    '-': [0x00,0x00,0x00,0x3F,0x00,0x00,0x00,0x00],
    '.': [0x00,0x00,0x00,0x00,0x00,0x0C,0x0C,0x00],
    '/': [0x60,0x30,0x18,0x0C,0x06,0x03,0x01,0x00],
    '0': [0x3E,0x63,0x73,0x7B,0x6F,0x67,0x3E,0x00],
    '1': [0x0C,0x0E,0x0C,0x0C,0x0C,0x0C,0x3F,0x00],
    '2': [0x1E,0x33,0x30,0x1C,0x06,0x33,0x3F,0x00],
    '3': [0x1E,0x33,0x30,0x1C,0x30,0x33,0x1E,0x00],
    '4': [0x38,0x3C,0x36,0x33,0x7F,0x30,0x78,0x00],
    '5': [0x3F,0x03,0x1F,0x30,0x30,0x33,0x1E,0x00],
    '6': [0x1C,0x06,0x03,0x1F,0x33,0x33,0x1E,0x00],
    '7': [0x3F,0x33,0x30,0x18,0x0C,0x0C,0x0C,0x00],
    '8': [0x1E,0x33,0x33,0x1E,0x33,0x33,0x1E,0x00],
    '9': [0x1E,0x33,0x33,0x3E,0x30,0x18,0x0E,0x00],
    ':': [0x00,0x0C,0x0C,0x00,0x00,0x0C,0x0C,0x00],
    ';': [0x00,0x0C,0x0C,0x00,0x00,0x0C,0x0C,0x06],
    '<': [0x18,0x0C,0x06,0x03,0x06,0x0C,0x18,0x00],
    '=': [0x00,0x00,0x3F,0x00,0x00,0x3F,0x00,0x00],
    '>': [0x06,0x0C,0x18,0x30,0x18,0x0C,0x06,0x00],
    '?': [0x1E,0x33,0x30,0x18,0x0C,0x00,0x0C,0x00],
    '@': [0x3E,0x63,0x7B,0x7B,0x7B,0x03,0x1E,0x00],
    'A': [0x0C,0x1E,0x33,0x33,0x3F,0x33,0x33,0x00],
    'B': [0x3F,0x66,0x66,0x3E,0x66,0x66,0x3F,0x00],
    'C': [0x3C,0x66,0x03,0x03,0x03,0x66,0x3C,0x00],
    'D': [0x1F,0x36,0x66,0x66,0x66,0x36,0x1F,0x00],
    'E': [0x7F,0x46,0x16,0x1E,0x16,0x46,0x7F,0x00],
    'F': [0x7F,0x46,0x16,0x1E,0x16,0x06,0x0F,0x00],
    'G': [0x3C,0x66,0x03,0x03,0x73,0x66,0x7C,0x00],
    'H': [0x33,0x33,0x33,0x3F,0x33,0x33,0x33,0x00],
    'I': [0x1E,0x0C,0x0C,0x0C,0x0C,0x0C,0x1E,0x00],
    'J': [0x78,0x30,0x30,0x30,0x33,0x33,0x1E,0x00],
    'K': [0x67,0x66,0x36,0x1E,0x36,0x66,0x67,0x00],
    'L': [0x0F,0x06,0x06,0x06,0x46,0x66,0x7F,0x00],
    'M': [0x63,0x77,0x7F,0x7F,0x6B,0x63,0x63,0x00],
    'N': [0x63,0x67,0x6F,0x7B,0x73,0x63,0x63,0x00],
    'O': [0x1C,0x36,0x63,0x63,0x63,0x36,0x1C,0x00],
    'P': [0x3F,0x66,0x66,0x3E,0x06,0x06,0x0F,0x00],
    'Q': [0x1E,0x33,0x33,0x33,0x3B,0x1E,0x38,0x00],
    'R': [0x3F,0x66,0x66,0x3E,0x36,0x66,0x67,0x00],
    'S': [0x1E,0x33,0x07,0x0E,0x38,0x33,0x1E,0x00],
    'T': [0x3F,0x2D,0x0C,0x0C,0x0C,0x0C,0x1E,0x00],
    'U': [0x33,0x33,0x33,0x33,0x33,0x33,0x3F,0x00],
    'V': [0x33,0x33,0x33,0x33,0x33,0x1E,0x0C,0x00],
    'W': [0x63,0x63,0x63,0x6B,0x7F,0x77,0x63,0x00],
    'X': [0x63,0x63,0x36,0x1C,0x1C,0x36,0x63,0x00],
    'Y': [0x33,0x33,0x33,0x1E,0x0C,0x0C,0x1E,0x00],
    'Z': [0x7F,0x63,0x31,0x18,0x4C,0x66,0x7F,0x00],
    '[': [0x1E,0x06,0x06,0x06,0x06,0x06,0x1E,0x00],
    '\\': [0x03,0x06,0x0C,0x18,0x30,0x60,0x40,0x00],
    ']': [0x1E,0x18,0x18,0x18,0x18,0x18,0x1E,0x00],
    '^': [0x08,0x1C,0x36,0x63,0x00,0x00,0x00,0x00],
    '_': [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF],
    '`': [0x0C,0x0C,0x18,0x00,0x00,0x00,0x00,0x00],
    'a': [0x00,0x00,0x1E,0x30,0x3E,0x33,0x6E,0x00],
    'b': [0x07,0x06,0x06,0x3E,0x66,0x66,0x3B,0x00],
    'c': [0x00,0x00,0x1E,0x33,0x03,0x33,0x1E,0x00],
    'd': [0x38,0x30,0x30,0x3e,0x33,0x33,0x6E,0x00],
    'e': [0x00,0x00,0x1E,0x33,0x3f,0x03,0x1E,0x00],
    'f': [0x1C,0x36,0x06,0x0f,0x06,0x06,0x0F,0x00],
    'g': [0x00,0x00,0x6E,0x33,0x33,0x3E,0x30,0x1F],
    'h': [0x07,0x06,0x36,0x6E,0x66,0x66,0x67,0x00],
    'i': [0x0C,0x00,0x0E,0x0C,0x0C,0x0C,0x1E,0x00],
    'j': [0x30,0x00,0x30,0x30,0x30,0x33,0x33,0x1E],
    'k': [0x07,0x06,0x66,0x36,0x1E,0x36,0x67,0x00],
    'l': [0x0E,0x0C,0x0C,0x0C,0x0C,0x0C,0x1E,0x00],
    'm': [0x00,0x00,0x33,0x7F,0x7F,0x6B,0x63,0x00],
    'n': [0x00,0x00,0x1F,0x33,0x33,0x33,0x33,0x00],
    'o': [0x00,0x00,0x1E,0x33,0x33,0x33,0x1E,0x00],
    'p': [0x00,0x00,0x3B,0x66,0x66,0x3E,0x06,0x0F],
    'q': [0x00,0x00,0x6E,0x33,0x33,0x3E,0x30,0x78],
    'r': [0x00,0x00,0x3B,0x6E,0x66,0x06,0x0F,0x00],
    's': [0x00,0x00,0x3E,0x03,0x1E,0x30,0x1F,0x00],
    't': [0x08,0x0C,0x3E,0x0C,0x0C,0x2C,0x18,0x00],
    'u': [0x00,0x00,0x33,0x33,0x33,0x33,0x6E,0x00],
    'v': [0x00,0x00,0x33,0x33,0x33,0x1E,0x0C,0x00],
    'w': [0x00,0x00,0x63,0x6B,0x7F,0x7F,0x36,0x00],
    'x': [0x00,0x00,0x63,0x36,0x1C,0x36,0x63,0x00],
    'y': [0x00,0x00,0x33,0x33,0x33,0x3E,0x30,0x1F],
    'z': [0x00,0x00,0x3F,0x19,0x0C,0x26,0x3F,0x00],
    '{': [0x38,0x0C,0x0C,0x07,0x0C,0x0C,0x38,0x00],
    '|': [0x18,0x18,0x18,0x00,0x18,0x18,0x18,0x00],
    '}': [0x07,0x0C,0x0C,0x38,0x0C,0x0C,0x07,0x00],
    '~': [0x6E,0x3B,0x00,0x00,0x00,0x00,0x00,0x00],
}

CHAR_W   = 8
CHAR_H   = 8
CHAR_GAP = 1


# ---------------------------------------------------------------------------
# Rasterisation
# ---------------------------------------------------------------------------

def rasterise_bitmap(text: str):
    """Use built-in 8×8 font. Returns (pixels, total_w, total_h)."""
    pixels   = []
    x_cursor = 0
    for ch in text:
        glyph = FONT8X8.get(ch, FONT8X8.get('?', [0] * 8))
        for row, byte in enumerate(glyph):
            for bit in range(8):
                if byte & (1 << bit):
                    pixels.append((x_cursor + bit, row))
        x_cursor += CHAR_W + CHAR_GAP
    return pixels, x_cursor - CHAR_GAP, CHAR_H


def rasterise_truetype(text: str, font_path: str, font_size: int, threshold: int):
    """Use a TrueType font via Pillow. Falls back to bitmap on failure."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("[warn] Pillow not installed — falling back to bitmap font.", file=sys.stderr)
        return rasterise_bitmap(text)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception as exc:
        print(f"[warn] Could not load '{font_path}': {exc} — falling back.", file=sys.stderr)
        return rasterise_bitmap(text)

    dummy = Image.new("L", (1, 1))
    bbox  = ImageDraw.Draw(dummy).textbbox((0, 0), text, font=font)
    w, h  = bbox[2] - bbox[0], bbox[3] - bbox[1]

    img  = Image.new("L", (w, h), 0)
    ImageDraw.Draw(img).text((-bbox[0], -bbox[1]), text, font=font, fill=255)

    pixels = [(x, y) for y in range(h) for x in range(w)
              if img.getpixel((x, y)) >= threshold]
    return pixels, w, h


# ---------------------------------------------------------------------------
# NDC conversion
# ---------------------------------------------------------------------------

def pixels_to_ndc_quads(pixels, total_w, total_h, scale, y_offset,
                         pixel_margin=0.05):
    """
    Each lit pixel → two CCW triangles (a screen-aligned quad) in NDC.
    Returns a flat list of (x, y) floats, 6 entries per source pixel.
    """
    px_w   = (2.0 * scale) / total_w
    px_h   = (2.0 * scale * total_h / total_w) / total_h
    inset  = pixel_margin * min(px_w, px_h)
    orig_x = -scale
    orig_y = scale * total_h / total_w + y_offset   # top-left y in NDC

    quads = []
    for col, row in pixels:
        l = orig_x +  col      * px_w + inset
        r = orig_x + (col + 1) * px_w - inset
        t = orig_y -  row      * px_h - inset
        b = orig_y - (row + 1) * px_h + inset
        quads += [(l, t), (l, b), (r, b),   # tri 1
                  (l, t), (r, b), (r, t)]   # tri 2

    return quads


# ---------------------------------------------------------------------------
# C++ snippet generation
# ---------------------------------------------------------------------------

def build_vertex_block(quads, color):
    """
    Return the lines that go *between* the sentinel comments, indented to
    match the surrounding sceneInit() body (4 spaces).
    """
    r, g, b = color
    lines = [
        f"    // {len(quads)} vertices  "
        f"({len(quads)//6} px-quads, {len(quads)//3} triangles)",
        "    struct Vertex { float position[3]; float color[3]; };",
        "    static const Vertex vertices[] =",
        "    {",
    ]
    for x, y in quads:
        lines.append(
            f"        {{ {{ {x:+.6f}f, {y:+.6f}f, 0.0f }}, "
            f"{{ {r:.2f}f, {g:.2f}f, {b:.2f}f }} }},"
        )
    lines.append("    };")
    return "\n".join(lines)


def emit_snippet(quads, color, bg_color, text):
    """
    Produce the standalone snippet (for --output / stdout mode).
    Shows the three edits needed if the user is patching manually.
    """
    r, g, b   = color
    br, bg_c, bb = bg_color
    n = len(quads)
    block = build_vertex_block(quads, color)

    return "\n".join([
        f"// Generated by text_to_vertices.py | text={repr(text)}",
        f"// Paste the vertex block between the sentinel comments in sceneInit().",
        "",
        f"// ① Replace glClearColor line in sceneRender() with:",
        f"//   glClearColor(/*<<<BG_COLOR>>>*/ {br:.2f}f, {bg_c:.2f}f, {bb:.2f}f, 1.0f /*<<<BG_COLOR_END>>>*/);",
        "",
        f"// ② Replace the vertex count in glDrawArrays:",
        f"//   glDrawArrays(GL_TRIANGLES, 0, /*<<<VERTEX_COUNT>>>*/ {n} /*<<<VERTEX_COUNT_END>>>*/);",
        "",
        f"// ③ Replace content between sentinels in sceneInit():",
        f"// {VERTS_BEGIN}",
        block,
        f"// {VERTS_END}",
    ])


# ---------------------------------------------------------------------------
# In-place patcher
# ---------------------------------------------------------------------------

def patch_file(path: Path, quads, color, bg_color, backup: bool):
    """
    Rewrite *path* in-place, replacing all three sentinel regions.
    Raises RuntimeError if any sentinel is missing.
    """
    src = path.read_text(encoding="utf-8")

    # ── 1. Vertex block ───────────────────────────────────────────────────
    begin_idx = src.find(VERTS_BEGIN)
    end_idx   = src.find(VERTS_END)
    if begin_idx == -1 or end_idx == -1 or end_idx < begin_idx:
        raise RuntimeError(
            f"Could not find sentinel pair\n  {VERTS_BEGIN}\n  {VERTS_END}\n"
            f"in {path}.\nAdd them to main.cpp or use the provided template."
        )

    # Preserve the indentation / newline immediately before END sentinel
    after_begin = src.index("\n", begin_idx) + 1   # first char after BEGIN line
    new_block   = build_vertex_block(quads, color)
    src = src[:after_begin] + new_block + "\n" + src[end_idx:]

    # ── 2. glDrawArrays count ─────────────────────────────────────────────
    n = len(quads)
    if not COUNT_RE.search(src):
        raise RuntimeError(
            "Could not find the VERTEX_COUNT sentinel in glDrawArrays.\n"
            "Expected pattern:\n"
            "  glDrawArrays(GL_TRIANGLES, 0, /*<<<VERTEX_COUNT>>>*/ N /*<<<VERTEX_COUNT_END>>>*/);"
        )
    src = COUNT_RE.sub(COUNT_REPL.format(count=n), src)

    # ── 3. glClearColor ───────────────────────────────────────────────────
    br, bg_c, bb = bg_color
    if not BGCOL_RE.search(src):
        raise RuntimeError(
            "Could not find the BG_COLOR sentinel in glClearColor.\n"
            "Expected pattern:\n"
            "  glClearColor(/*<<<BG_COLOR>>>*/ ... /*<<<BG_COLOR_END>>>*/);"
        )
    src = BGCOL_RE.sub(
        BGCOL_REPL.format(r=f"{br:.2f}", g=f"{bg_c:.2f}", b=f"{bb:.2f}"),
        src
    )

    # ── Write ─────────────────────────────────────────────────────────────
    if backup:
        shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
        print(f"[info] Backup written to '{path}.bak'", file=sys.stderr)

    path.write_text(src, encoding="utf-8")
    print(f"[info] Patched '{path}'  ({n} vertices)", file=sys.stderr)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Convert text to OpenGL vertices and optionally patch main.cpp."
    )
    ap.add_argument("text",
                    help="Text to render")
    ap.add_argument("--patch", metavar="MAIN_CPP",
                    help="Path to main.cpp to patch in-place (uses sentinel comments)")
    ap.add_argument("--backup", action="store_true",
                    help="Keep MAIN_CPP.bak before patching (requires --patch)")
    ap.add_argument("--font", default=None,
                    help="Path to .ttf/.otf font (omit = built-in 8×8 bitmap font)")
    ap.add_argument("--font-size", type=int, default=48,
                    help="Font size in px for TrueType mode (default: 48)")
    ap.add_argument("--color", type=float, nargs=3, default=[1.0, 1.0, 1.0],
                    metavar=("R", "G", "B"),
                    help="Text colour, 0-1 floats (default: 1 1 1 = white)")
    ap.add_argument("--bg-color", type=float, nargs=3, default=[0.2, 0.3, 0.3],
                    metavar=("R", "G", "B"),
                    help="Background glClearColor (default: 0.2 0.3 0.3)")
    ap.add_argument("--scale", type=float, default=0.9,
                    help="NDC horizontal scale 0-1 (default: 0.9)")
    ap.add_argument("--y-offset", type=float, default=0.0,
                    help="Vertical NDC offset -1..1 (default: 0.0)")
    ap.add_argument("--threshold", type=int, default=128,
                    help="Alpha threshold for lit pixels in TrueType mode (default: 128)")
    ap.add_argument("--output", default=None,
                    help="Write snippet to this file instead of stdout")
    args = ap.parse_args()

    # ── Rasterise ──────────────────────────────────────────────────────────
    if args.font:
        pixels, w, h = rasterise_truetype(
            args.text, args.font, args.font_size, args.threshold)
    else:
        pixels, w, h = rasterise_bitmap(args.text)

    if not pixels:
        sys.exit("[error] No pixels generated — check your text/font.")

    print(f"[info] Rasterised {len(pixels)} lit pixels ({w}×{h} grid)", file=sys.stderr)

    # ── NDC conversion ─────────────────────────────────────────────────────
    quads = pixels_to_ndc_quads(pixels, w, h, args.scale, args.y_offset)
    print(f"[info] {len(quads)} vertices  ({len(quads)//3} triangles)", file=sys.stderr)

    # ── Patch mode ─────────────────────────────────────────────────────────
    if args.patch:
        try:
            patch_file(Path(args.patch), quads, args.color, args.bg_color,
                       args.backup)
        except RuntimeError as exc:
            sys.exit(f"[error] {exc}")
        return   # don't also dump to stdout

    # ── Snippet mode ───────────────────────────────────────────────────────
    snippet = emit_snippet(quads, args.color, args.bg_color, args.text)
    if args.output:
        Path(args.output).write_text(snippet, encoding="utf-8")
        print(f"[info] Snippet written to '{args.output}'", file=sys.stderr)
    else:
        print(snippet)


if __name__ == "__main__":
    main()

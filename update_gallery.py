#!/usr/bin/env python3
"""
Run this script from the repo root whenever you add files to assets/img/:
    python update_gallery.py
It will rebuild the gallery grid in gallery.html automatically.
"""

import os
import re

IMG_DIR = "assets/img"
GALLERY_FILE = "gallery.html"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
VIDEO_EXTS = {".mp4", ".webm", ".mov"}

def make_cell(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    url = filepath.replace("\\", "/")
    if ext in VIDEO_EXTS:
        return f'''    <div style="aspect-ratio: 4/3; border-radius: 8px; overflow: hidden; border: 1px solid var(--divider); background: var(--card-bg);">
      <video autoplay loop muted playsinline style="width:100%; height:100%; object-fit:cover;">
        <source src="{url}" type="video/mp4">
      </video>
    </div>'''
    else:
        return f'''    <div style="aspect-ratio: 4/3; border-radius: 8px; overflow: hidden; border: 1px solid var(--divider); background: var(--card-bg);">
      <img src="{url}" style="width:100%; height:100%; display:block; object-fit:cover;">
    </div>'''

# Collect files
files = sorted(
    f for f in os.listdir(IMG_DIR)
    if os.path.splitext(f)[1].lower() in IMAGE_EXTS | VIDEO_EXTS
)

if not files:
    print("No images or videos found in", IMG_DIR)
    exit()

cells = "\n\n".join(make_cell(os.path.join(IMG_DIR, f)) for f in files)
grid = f'  <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">\n\n{cells}\n\n  </div>'

# Read gallery.html
with open(GALLERY_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Replace everything between the h1 and the footer
new_html = re.sub(
    r'(<h1[^>]*>Gallery</h1>\s*<p[^>]*>.*?</p>).*?(<footer)',
    lambda m: m.group(1) + "\n\n" + grid + "\n</div>\n\n" + m.group(2),
    html,
    flags=re.DOTALL
)

with open(GALLERY_FILE, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"Gallery updated with {len(files)} file(s):")
for f in files:
    print(f"  • {f}")

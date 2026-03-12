#!/usr/bin/env python3
"""Generate Breathe app icon — minimal dark with soft purple orb + glow."""
from PIL import Image, ImageDraw, ImageFilter
import os, subprocess, shutil

def draw_icon(size):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size / 2, size * 0.48
    r_corner = int(size * 0.222)

    # Dark background
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=r_corner, fill=(10, 10, 26, 255))

    # Soft glow — drawn on separate layer, blurred, composited at low opacity
    glow_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_r = int(size * 0.22)
    glow_draw.ellipse([cx - glow_r, cy - glow_r, cx + glow_r, cy + glow_r],
                       fill=(120, 80, 240, 255))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=size * 0.12))

    # Composite glow at ~20% opacity
    glow_arr = list(glow_layer.getdata())
    faded = [(r, g, b, int(a * 0.22)) for r, g, b, a in glow_arr]
    glow_faded = Image.new('RGBA', (size, size))
    glow_faded.putdata(faded)
    img = Image.alpha_composite(img, glow_faded)

    # Main orb
    orb_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    orb_draw = ImageDraw.Draw(orb_layer)
    orb_r = int(size * 0.155)
    for i in range(orb_r, 0, -1):
        t = 1 - (i / orb_r)
        r = int(88 + 65 * t)
        g = int(75 + 45 * t)
        b = int(228 + 22 * t)
        a = int(210 + 45 * t)
        bbox = [cx - i, cy - i, cx + i, cy + i]
        orb_draw.ellipse(bbox, fill=(r, g, b, a))

    # Inner highlight
    hl_cx = cx - orb_r * 0.2
    hl_cy = cy - orb_r * 0.2
    for i in range(int(orb_r * 0.4), 0, -1):
        t = 1 - (i / (orb_r * 0.4))
        a = int(30 * t)
        bbox = [hl_cx - i, hl_cy - i, hl_cx + i, hl_cy + i]
        orb_draw.ellipse(bbox, fill=(255, 255, 255, a))

    img = Image.alpha_composite(img, orb_layer)

    return img

print("Generating 1024x1024 master icon...")
master = draw_icon(1024)

iconset_path = "/Users/bertomill/setting reminder to breathe every night at 9pm/AppIcon.iconset"
os.makedirs(iconset_path, exist_ok=True)

sizes = [
    (16, "icon_16x16.png"), (32, "icon_16x16@2x.png"),
    (32, "icon_32x32.png"), (64, "icon_32x32@2x.png"),
    (128, "icon_128x128.png"), (256, "icon_128x128@2x.png"),
    (256, "icon_256x256.png"), (512, "icon_256x256@2x.png"),
    (512, "icon_512x512.png"), (1024, "icon_512x512@2x.png"),
]

for sz, name in sizes:
    resized = master.resize((sz, sz), Image.LANCZOS) if sz != 1024 else master
    resized.save(os.path.join(iconset_path, name))
    print(f"  {name}")

icns_path = "/Users/bertomill/setting reminder to breathe every night at 9pm/AppIcon.icns"
subprocess.run(["iconutil", "-c", "icns", iconset_path, "-o", icns_path], check=True)
print(f"Created {icns_path}")
shutil.rmtree(iconset_path)
print("Done.")

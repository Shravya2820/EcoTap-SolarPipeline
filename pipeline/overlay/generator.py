"""
generator.py
Creates an overlay visualization:
- Base satellite image
- Rooftop buffer polygon
- Solar panel simulation grid
"""

from PIL import Image, ImageDraw
from shapely.geometry import Point
import math


def draw_overlay(img_path, polygon, output_path, panel_w=1.0, panel_h=2.0):
    """
    img_path: satellite image path (JPG/PNG)
    polygon: shapely Polygon in lat/lon
    output_path: save overlay image
    """

    # Open satellite raster
    base = Image.open(img_path).convert("RGBA")
    draw = ImageDraw.Draw(base, "RGBA")

    # ----------------------------
    # 1. Normalize polygon coordinates to image pixels
    # ----------------------------
    poly_coords = list(polygon.exterior.coords)

    min_x = min(p[0] for p in poly_coords)
    max_x = max(p[0] for p in poly_coords)
    min_y = min(p[1] for p in poly_coords)
    max_y = max(p[1] for p in poly_coords)

    def to_pixel(p):
        px = (p[0] - min_x) / (max_x - min_x + 1e-9) * base.width
        py = (p[1] - min_y) / (max_y - min_y + 1e-9) * base.height
        return (px, py)

    pixel_poly = [to_pixel(p) for p in poly_coords]

    # Draw the rooftop buffer mask
    draw.polygon(pixel_poly, fill=(0, 255, 0, 80), outline=(0, 255, 0, 200))

    # ----------------------------
    # 2. Simulate panel grid placement
    # ----------------------------
    panel_w_px = base.width / 20
    panel_h_px = base.height / 15

    panel_count = 0

    for x in range(0, base.width, int(panel_w_px + 3)):
        for y in range(0, base.height, int(panel_h_px + 3)):

            cx = x + panel_w_px / 2
            cy = y + panel_h_px / 2

            # Map pixel center → geo-coordinates
            gx = min_x + (cx / base.width) * (max_x - min_x)
            gy = min_y + (cy / base.height) * (max_y - min_y)

            # ✔ FIXED: Must use a Shapely Point(gx, gy)
            if polygon.contains(Point(gx, gy)):
                rect = [
                    (x, y),
                    (x + panel_w_px, y),
                    (x + panel_w_px, y + panel_h_px),
                    (x, y + panel_h_px),
                ]
                draw.rectangle(rect, fill=(255, 255, 0, 120), outline=(255, 255, 0, 180))
                panel_count += 1

    # Save output image
    base.save(output_path)

    # ----------------------------
    # 3. Estimate solar capacity
    # ----------------------------
    total_kw = panel_count * 0.55  # each panel = 550W → 0.55 kW

    return {
        "panel_count": panel_count,
        "total_kw": total_kw,
        "overlay_path": str(output_path)
    }
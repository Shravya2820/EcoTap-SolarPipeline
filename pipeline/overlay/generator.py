from PIL import Image, ImageDraw
from shapely.geometry import Point, Polygon


def draw_overlay(img_path, polygon: Polygon, output_path, panel_w=1.0, panel_h=2.0):
    """
    Creates overlay visualization with:
    - Base satellite image
    - Rooftop buffer polygon
    - Solar panel simulation grid
    """
    # ----------------------------------------------------------------------
    # 1. Load base satellite image
    # ----------------------------------------------------------------------
    base = Image.open(img_path).convert("RGBA")
    draw = ImageDraw.Draw(base, "RGBA")

    # ----------------------------------------------------------------------
    # 2. Extract polygon coords and map to pixel space
    # ----------------------------------------------------------------------
    poly_coords = list(polygon.exterior.coords)

    min_x = min(p[0] for p in poly_coords)
    max_x = max(p[0] for p in poly_coords)
    min_y = min(p[1] for p in poly_coords)
    max_y = max(p[1] for p in poly_coords)

    def to_pixel(pt):
        px = (pt[0] - min_x) / (max_x - min_x + 1e-9) * base.width
        py = (pt[1] - min_y) / (max_y - min_y + 1e-9) * base.height
        return (px, py)

    pixel_poly = [to_pixel(p) for p in poly_coords]

    draw.polygon(pixel_poly, fill=(0, 255, 0, 80), outline=(0, 255, 0, 200))

    # ----------------------------------------------------------------------
    # 3. Panel placement simulation
    # ----------------------------------------------------------------------
    panel_w_px = base.width / 20
    panel_h_px = base.height / 15

    panel_count = 0

    for x in range(0, base.width, int(panel_w_px + 3)):
        for y in range(0, base.height, int(panel_h_px + 3)):

            cx = x + panel_w_px / 2
            cy = y + panel_h_px / 2

            # Pixel → geo conversion
            gx = min_x + (cx / base.width) * (max_x - min_x)
            gy = min_y + (cy / base.height) * (max_y - min_y)

            # Correct Shapely check
            if polygon.contains(Point(gx, gy)):
                rect = [
                    (x, y),
                    (x + panel_w_px, y),
                    (x + panel_w_px, y + panel_h_px),
                    (x, y + panel_h_px),
                ]
                draw.rectangle(rect, fill=(255, 255, 0, 120), outline=(255, 255, 0, 200))
                panel_count += 1

    # ----------------------------------------------------------------------
    # 4. Save final overlay
    # ----------------------------------------------------------------------
    base.save(output_path)

    return {
        "panel_count": panel_count,
        "total_kw": round(panel_count * 0.55, 2),
        "overlay_path": output_path
    }
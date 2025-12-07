#!/usr/bin/env python3
"""
EcoTap – Full Inference Pipeline

1. Read coordinates from inputs/sites.xlsx
2. Fetch satellite image (ESRI by default)
3. Generate buffer polygon (Shapely)
4. Draw overlay (panel simulation)
5. Save JSON + PNG outputs
"""

import os
import json
import argparse
from pathlib import Path

import pandas as pd
from tqdm import tqdm

# --- our modules ---
from pipeline.fetcher.fetcher import ImageFetcher
from pipeline.preprocessing.utils import compute_buffer_and_metadata
from pipeline.overlay.generator import draw_overlay


# ----------------------------
# Helpers
# ----------------------------
def ensure_dir(p: Path):
    """Create folder if missing."""
    p.mkdir(parents=True, exist_ok=True)


# ----------------------------
# Per–row processing
# ----------------------------
def process_row(row, outputs_dir: Path, fetcher):
    sid = int(row["sample_id"])
    lat = float(row["latitude"])
    lon = float(row["longitude"])

    # 1. Fetch satellite image
    try:
        img_path, metadata = fetcher.fetch(
            sample_id=sid,
            lat=lat,
            lon=lon,
            zoom=20
        )
    except Exception as e:
        print(f"[ERROR] Fetch failed for {sid}: {e}")
        return

    # 2. Compute buffer polygon (Shapely)
    try:
        buffer_poly, area_sqft = compute_buffer_and_metadata(lat, lon)
    except Exception as e:
        print(f"[ERROR] Buffer computation failed for {sid}: {e}")
        return

    # 3. Draw overlay
    overlay_path = outputs_dir / f"{sid}_overlay.png"

    try:
        overlay_info = draw_overlay(
            img_path=img_path,
            polygon=buffer_poly,
            output_path=str(overlay_path)
        )
    except Exception as e:
        print(f"[ERROR] Overlay failed for {sid}: {e}")
        return

    # 4. Prepare output JSON
    result = {
        "sample_id": sid,
        "lat": lat,
        "lon": lon,

        "image_metadata": metadata,

        "buffer_polygon_wkt": buffer_poly.wkt,
        "buffer_area_sqft": area_sqft,

        "panel_count": overlay_info.get("panel_count", 0),
        "total_kw": overlay_info.get("total_kw", 0.0),

        "overlay_image": overlay_path.name,
        "qc_status": "AUTO_GENERATED"
    }

    # 5. Save JSON
    json_path = outputs_dir / f"{sid}.json"
    json_path.write_text(json.dumps(result, indent=2))


# ----------------------------
# Main
# ----------------------------
def main(args):
    input_xlsx = Path(args.input_xlsx)
    outputs_dir = Path(args.output_folder)

    ensure_dir(outputs_dir)
    ensure_dir(Path("data/raw"))

    if not input_xlsx.exists():
        raise FileNotFoundError(f"Input XLSX not found: {input_xlsx}")

    df = pd.read_excel(input_xlsx)

    # Required columns
    required = {"sample_id", "latitude", "longitude"}
    if not required.issubset(df.columns):
        raise ValueError(f"Input .xlsx must contain columns: {required}")

    df = df.fillna("")

    fetcher = ImageFetcher(provider_name="esri")

    print("\nStarting inference...\n")

    for _, row in tqdm(df.iterrows(), total=len(df)):
        process_row(row, outputs_dir, fetcher)

    print(f"\n✔ Done! Outputs generated in: {outputs_dir}\n")


# ----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_xlsx", default="inputs/sites.xlsx")
    parser.add_argument("--output_folder", default="outputs")
    args = parser.parse_args()
    main(args)

#!/usr/bin/env python3
"""
Full Inference Pipeline
1. Reads coordinates from inputs/sites.xlsx
2. Fetches satellite image (ESRI by default)
3. Computes buffer polygon + area using Shapely
4. Generates a solar-panel overlay image
5. Writes JSON analysis + PNG overlay into outputs/
"""

import os
import json
import argparse
from pathlib import Path

import pandas as pd
from tqdm import tqdm

# --- custom modules ---
from pipeline.fetcher.fetcher import ImageFetcher
from pipeline.preprocessing.utils import compute_buffer_and_metadata
from pipeline.overlay.generator import draw_overlay

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def process_row(row, outputs_dir: Path, fetcher):
    sid = int(row["sample_id"])

    # -------------------
    # 1. Fetch satellite image
    # -------------------
    try:
        img_path, metadata = fetcher.fetch(
            sample_id=sid,
            lat=row["latitude"],
            lon=row["longitude"],
            zoom=20
        )
    except Exception as e:
        print(f"[ERROR] Failed to fetch satellite for {sid}: {e}")
        return

    # -------------------
    # 2. Compute buffer polygon + sqft
    # -------------------
    buffer_poly, area_sqft = compute_buffer_and_metadata(
        row["latitude"],
        row["longitude"]
    )

    # -------------------
    # 3. Generate overlay image
    # -------------------
    overlay_path = outputs_dir / f"{sid}_overlay.png"

    try:
        overlay_data = draw_overlay(
            img_path=img_path,
            polygon=buffer_poly,
            output_path=overlay_path
        )
    except Exception as e:
        print(f"[ERROR] Failed to create overlay for {sid}: {e}")
        return

    # -------------------
    # 4. Prepare JSON data
    # -------------------
    json_data = {
        "sample_id": sid,
        "lat": float(row["latitude"]),
        "lon": float(row["longitude"]),
        "image_metadata": metadata,

        "buffer_polygon_wkt": buffer_poly.wkt,
        "buffer_area_sqft": area_sqft,

        "panel_count": overlay_data["panel_count"],
        "total_kw": overlay_data["total_kw"],
        "overlay_image": str(overlay_path.name),

        "qc_status": "AUTO_GENERATED",
    }

    # -------------------
    # 5. Write JSON
    # -------------------
    json_path = outputs_dir / f"{sid}.json"
    json_path.write_text(json.dumps(json_data, indent=2))


def main(args):
    input_xlsx = Path(args.input_xlsx)
    outputs_dir = Path(args.output_folder)

    ensure_dir(outputs_dir)
    ensure_dir(Path("data/raw"))

    if not input_xlsx.exists():
        print(f"[ERROR] Input file not found: {input_xlsx}")
        return

    df = pd.read_excel(input_xlsx)

    required_cols = {"sample_id", "latitude", "longitude"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Input xlsx must contain columns: {required_cols}")

    df = df.fillna("")

    fetcher = ImageFetcher(provider_name="esri")

    print("\nStarting inference...\n")

    for _, row in tqdm(df.iterrows(), total=len(df)):
        process_row(row, outputs_dir, fetcher)

    print(f"\n✔ Done! Outputs generated in: {outputs_dir}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_xlsx", default="inputs/sites.xlsx")
    parser.add_argument("--output_folder", default="outputs")
    args = parser.parse_args()
    main(args)
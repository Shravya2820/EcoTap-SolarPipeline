# Testing Report — v1

**Date:** 2025-12-06
**Author:** Shravya N Bhat

## 1. Test summary
Run 1: 2 sample inputs from inputs/sites.xlsx

## 2. Samples used
- sample_id 1 — lat, lon
- sample_id 2 — lat, lon

## 3. Outputs (attach JSON + overlay images)
- outputs/1.json — (paste JSON snippet)
- outputs/1_overlay.png — (include screenshot)

## 4. QC checks (format)
- Required keys present: sample_id, lat, lon, has_solar, confidence, pv_area_sqm_est, buffer_radius_sqft, qc_status, bbox_or_mask, image_metadata — PASS/FAIL

## 5. Notes on results
- Observations about panel detection, false positives, overlay alignment.

## 6. Action items
- Fix overlay coordinate→pixel transformation (if needed)
- Add additional 10 test locations (urban + rural)

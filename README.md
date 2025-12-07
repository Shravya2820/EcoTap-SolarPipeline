# EcoTap — Rooftop Solar Detection

## Project summary
EcoTap builds an auditable pipeline that detects rooftop solar panels from satellite imagery, estimates installed PV area using GSD and geometry logic, and writes per-sample JSON + overlay artifacts for verification.

## Features
- Satellite fetcher (ESRI / Google Static)
- Rooftop segmentation
- Solar panel segmentation
- Look-alike rejection classifier
- GSD-based pixel→sqm conversion
- QC status + explainability strings
- JSON + overlay outputs per sample

## Quick run (inference)
From repo root:

```bash
python -m pipeline.run_inference --input_xlsx inputs/sites.xlsx --output_folder outputs
---
Notes:
•	Ensure inputs/sites.xlsx has sample_id, latitude, longitude columns.
•	Outputs are written to outputs/ as <sample_id>.json and <sample_id>_overlay.png.

Where to find things
•	pipeline/ — inference + preprocessing code
•	models/ — trained model weights (placed here after training)
•	training/ — Colab & training scripts 
•	docs/ — this documentation, model card, diagrams, test reports

Roboflow integration 
See docs/roboflow_integration.md for the full integration guide and examples.

---

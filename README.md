<<<<<<< HEAD
# EcoInnovators Ideathon — PV Detection Pipeline

This repository contains the full solution pipeline for:
- Satellite image fetching
- Rooftop & solar panel detection
- Area estimation
- QC status generation
- JSON + overlay artifact generation

Current step: Pipeline skeleton with input reading and output placeholders.
=======
## Rooftop Solar Detection Pipeline  
🛠️ Automated rooftop PV detection & estimation system for Ideathon 2026  

## 🔎 Overview  
EcoTap Solar Detection Pipeline is a full-stack, auditable solution that:  
- Takes an Excel file with sample IDs and geographic coordinates (lat/lon)  
- Fetches high-resolution satellite imagery (via ESRI or Google Static Maps)  
- Segments rooftops, detects solar panels, rejects look-alikes, and estimates PV panel area  
- Produces clearly documented outputs (JSON, overlay image, QC metadata) ready for audits or large-scale solar mapping  

## 🚀 Features  

| Feature | Description |
|--------|-------------|
| **Automated Fetcher** | Downloads satellite imagery given coordinates, caches images + metadata |
| **Rooftop Segmentation** | Detects building rooftops to exclude non-roof areas (reduces false positives) |
| **Solar Detection** | Identifies solar panels on rooftops (segmentation / bounding boxes) |
| **Look-Alike Rejection** | Filters out non-solar objects (metal sheets, water tanks, skylights) using a small classifier |
| **Area Estimation** | Converts pixel area → real-world m² using GSD and geometric overlap logic |
| **Buffer Logic** | Applies 1200 sqft + 2400 sqft thresholds for valid rooftop solar detection |
| **QC & Explainability** | Outputs QC status, reasoning, capture metadata — ideal for audits |
| **Governance-Ready Output** | JSON + overlay + optional GeoJSON with complete metadata per sample |
| **Modular & Extensible** | Easy to plug new models or providers; clear separation of components |
| **Pipeline Logging & Caching** | Robust engineering: caching, retries, clean outputs, repeatable runs |

---

## 📁 Repository Structure  

```

EcoTap-SolarPipeline/
├── pipeline/                # Inference & preprocessing scripts
│   ├── run_inference.py     # Main entrypoint
│   ├── fetcher/             # Satellite image download + caching
│   ├── preprocessing/       # GSD, geometry, image normalization
│   ├── overlay/             # Overlay image generation (post-processing)
│   ├── model/               # Placeholder for ML models
│   └── utils/               # Shared utilities
├── models/                  # Final trained models (roof_seg, solar_det, lookalike_clf)
├── training/                # Colab + shell training scripts + configs
├── data/                    # Raw/processed imagery (cache)
│   ├── raw/
│   └── processed/
├── inputs/                  # Input Excel (sites.xlsx)
├── outputs/                 # Generated JSON + overlay images
├── docs/                    # Documentation (README, model card, diagrams, test reports)
├── environment/             # Env specification (requirements, conda env file)
├── LICENSE
└── .gitignore

```

---

## 📥 Input Specification  

- Input file: `inputs/sites.xlsx`  
- Required columns: `sample_id`, `latitude`, `longitude`  
- Sample format:

| sample_id | latitude   | longitude   |
|----------:|-----------:|------------:|
| 1         | 12.9716    | 77.5946     |

---

## 📤 Output Specification  

For each input row, the pipeline generates:

- `outputs/<sample_id>.json` — detailed metadata & detection results  
- `outputs/<sample_id>_overlay.png` — overlay image with rooftop & solar masks  
- Optional summary CSV / index file for bulk review  

Example JSON `"keys"` include:  
```

sample_id, lat, lon, has_solar, confidence, pv_area_sqm_est,
buffer_radius_sqft, qc_status, bbox_or_mask, image_metadata

````

---

## 🧑‍💻 How to Run  

```bash
# (optional) create virtual env or conda env  
# pip install -r environment/requirements.txt  

python -m pipeline.run_inference \
  --input_xlsx inputs/sites.xlsx \
  --output_folder outputs \
  --provider esri \
  --zoom 20
````

💡 For Google Static Maps provider, add `--provider google_static --api_key YOUR_KEY`.

---

## 🛠 Development & Extensibility

* To integrate new imagery providers: extend `pipeline/fetcher/`
* To add rooftop / solar detection ML models: place in `models/` and update pipeline logic
* To adjust QC logic or buffer thresholds: modify `pipeline/preprocessing/geometry.py` & QC module

---

## 📚 Documentation & Testing

See `/docs/` for:

* Model Card (`docs/model_card/MODEL_CARD.pdf`)
* System architecture diagram (`docs/diagrams/architecture.png`)
* Test reports (`docs/test_reports/`) — includes example JSON & overlay outputs

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.
>>>>>>> e5e99274817d2cfcad236db932c621aae4ace8c3

# Architecture diagram instructions 

Canvas size: 1600×900 px

Blocks (left to right):
- Inputs (XLSX)
- Fetcher (ESRI / Google Static) -> image cache
- Preprocessor (normalize, GSD estimate, QC)
- Rooftop Segmentation (Model A)
- Solar Detection (Model B)
- Look-alike Classifier (Model C)
- Geometry & Area Estimator (Shapely, GSD scaling)
- Explainability & QC module
- Output Writer (JSON + overlays)

Add arrows between each block. Add a side-note box for "Model artifacts (models/*)" and a "Logs & Audit" sink.

Export as PNG → save `docs/diagrams/architecture.png`.

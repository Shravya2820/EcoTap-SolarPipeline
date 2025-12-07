# Model Card — EcoTap Rooftop Solar Detection

## Model Overview
Two main models are used:
- **Rooftop segmentation** (YOLOv8-seg or lightweight UNet)
- **Solar panel segmentation** (YOLOv8-seg)

A small classifier (MobileNet/EfficientNet) is used for look-alike rejection.

## Training Data
- Roboflow datasets (as provided by ML teammate)
- Synthetic augmentation: synthetic panels, shadows, blur, compression

## Intended Use
- Automated rooftop solar verification for large-scale audits or subsidy validation.
- Not intended for safety-critical decision making without human verification.

## Limitations
- Poor performance under heavy cloud/shadow.
- Low-resolution imagery reduces detection recall.
- Small/tilted panels or highly reflective surfaces cause false positives.

## Known Failure Cases
- Metal sheets / corrugated roofs mistaken as panels.
- Water tanks and reflective surfaces.
- Dense tree canopy occlusion.

## Metrics & Evaluation
- Primary metrics to report: F1 (has_solar), mAP50 (segmentation), RMSE (area estimation).
- Validation: geographic k-fold to measure robustness across regions.

## Recommendations
- Retrain periodically with new geographies.
- Expand dataset for rural roof types and small panels.
- Add adversarial synthetic negatives for look-alike classifier.
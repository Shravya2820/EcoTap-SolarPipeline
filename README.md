# **EcoTap - Rooftop Solar Detection Pipeline**

EcoTap is an end-to-end, auditable pipeline designed to detect rooftop solar panels from satellite imagery, estimate solar PV area using geometric analysis + GSD scaling, and generate fully verifiable JSON + overlay outputs suitable for government evaluation.

---

## **🌞 Project Summary**

EcoTap processes latitude/longitude coordinates, fetches satellite imagery, applies rooftop + solar detection logic, computes usable rooftop area, and generates overlay visualizations along with structured JSON outputs.

This pipeline is built for:

* Ideathons
* Hackathons
* Renewable-energy audits
* Automated PV verification workflows

---

## **✨ Features**

### **✔ Image Fetching**

* ESRI satellite fetcher (default)
* Google Static Maps (optional)

### **✔ Rooftop + Solar Processing**

* Rooftop buffer computation (1200–2400 sqft logic)
* GSD-scaled pixel → square-meter estimation
* Panel placement simulation (fallback mode)

### **✔ QC & Explainability**

* Auto-generated QC flags
* Human-readable reasoning strings

### **✔ Output Artifacts**

For each sample:

* `<sample_id>.json`
* `<sample_id>_overlay.png`
* Metadata about source imagery, buffer polygon, panel count, and estimated kW

---

## **📂 Repository Structure**

```
pipeline/         → inference engine & modules  
models/           → trained ML models (after training)  
docs/             → model card, diagrams, reports, integration guides  
training/         → training scripts (Colab-ready)  
inputs/           → sites.xlsx  
outputs/          → all JSON + overlays generated  
environment/      → requirements & environment files  
```

---

## **▶ Quick Run (Inference)**

From repository root:

```bash
python -m pipeline.run_inference --input_xlsx inputs/sites.xlsx --output_folder outputs
```

**Important:**
Your `inputs/sites.xlsx` **must contain these columns exactly**:

| sample_id | latitude | longitude |
| --------- | -------- | --------- |

Outputs will be generated in:

```
outputs/<sample_id>.json
outputs/<sample_id>_overlay.png
```

---

## **📄 Documentation**

All documentation is included inside the `docs/` folder:

### **1. Model Card**

`docs/model_card/MODEL_CARD.pdf`
Includes training details, dataset, failure cases, limitations, and evaluation metrics.

### **2. Architecture Diagram**

`docs/diagrams/architecture.png`
Shows the entire system flow:
Fetcher → Preprocessing → Rooftop Seg → Solar Seg → QC → Outputs

### **3. Testing Reports**

`docs/test_reports/testing_v1.pdf`
Contains sample JSON, overlays, QC checks, and validation notes.

### **4. Roboflow Integration**

`docs/roboflow_integration.md`
Complete workflow API documentation (curl, Python, Node.js).

---
## **🤝 Team**

Shravya N Bhat
Shriya M
Shrinidhi Kati

---





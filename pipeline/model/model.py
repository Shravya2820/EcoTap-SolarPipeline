import os
import random
from shapely.geometry import Polygon

class DummyModel:
    """A lightweight fake model that returns deterministic sample polygons."""

    def predict_polygon(self):
        # Hardcoded small polygon (valid)
        return Polygon([
            (0.1, 0.1),
            (0.9, 0.1),
            (0.9, 0.9),
            (0.1, 0.9)
        ])

class ModelLoader:
    def __init__(self, model_path):
        self.model_path = model_path

        if not os.path.exists(model_path):
            print(f"[WARNING] Model not found: {model_path}. Using Dummy Model.")
            self.model = DummyModel()
        else:
            print(f"[INFO] Loaded model: {model_path} (dummy loader)")
            self.model = DummyModel()  # Still using dummy loader

    def run(self, image_path):
        """Return fake segmentation polygon as Shapely polygon."""
        return self.model.predict_polygon()

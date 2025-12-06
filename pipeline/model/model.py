"""
Lightweight placeholder ML model.
We are NOT using torch for now because training happens later.
This class just simulates inference output.
"""

class SolarPanelModel:
    def __init__(self):
        # No heavy ML model loaded
        self.name = "placeholder-model-v1"

    def predict(self, image_path):
        """
        Simulated prediction result.
        Later we will replace this with real ML inference.
        """
        return {
            "panel_count": 0,
            "total_kw": 0.0,
            "confidence": 0.0
        }


# Utility function used by pipeline
def load_model():
    """
    Returns a lightweight placeholder model.
    """
    return SolarPanelModel()

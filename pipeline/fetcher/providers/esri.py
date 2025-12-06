"""
ESRI World Imagery Provider
"""

import requests
import math
from pathlib import Path


class EsriProvider:
    def __init__(self):
        self.base_url = (
            "https://services.arcgisonline.com/ArcGIS/rest/services/"
            "World_Imagery/MapServer/tile"
        )

    def fetch_image(self, sample_id, lat, lon, zoom=20):
        # Convert lat/lon to tile index
        tile_x = int((lon + 180.0) / 360.0 * (2 ** zoom))
        tile_y = int(
            (1.0 - math.log(math.tan(math.radians(lat)) +
            (1 / math.cos(math.radians(lat)))) / math.pi)
            / 2.0 * (2 ** zoom)
        )

        url = f"{self.base_url}/{zoom}/{tile_y}/{tile_x}"

        response = requests.get(url)

        if response.status_code != 200:
            raise RuntimeError(f"ESRI imagery fetch failed: {response.status_code}")

        out_path = Path(f"data/raw/{sample_id}.jpg")
        out_path.write_bytes(response.content)

        metadata = {
            "source": "ESRI",
            "zoom": zoom,
            "lat": lat,
            "lon": lon
        }

        return out_path, metadata

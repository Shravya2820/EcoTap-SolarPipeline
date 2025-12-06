"""
Google Static Maps Provider
"""

import requests
from pathlib import Path


class GoogleStaticProvider:
    def __init__(self, api_key=None):
        self.base_url = "https://maps.googleapis.com/maps/api/staticmap"
        self.api_key = api_key

    def fetch_image(self, sample_id, lat, lon, zoom=20):
        if self.api_key is None:
            raise ValueError("GoogleStaticProvider requires a Google Maps API key.")

        params = {
            "center": f"{lat},{lon}",
            "zoom": zoom,
            "size": "640x640",
            "maptype": "satellite",
            "key": self.api_key
        }

        response = requests.get(self.base_url, params=params)

        if response.status_code != 200:
            raise RuntimeError(f"Google Static Maps API error: {response.status_code}")

        out_path = Path(f"data/raw/{sample_id}.jpg")
        out_path.write_bytes(response.content)

        metadata = {
            "source": "GoogleStatic",
            "zoom": zoom,
            "lat": lat,
            "lon": lon
        }

        return out_path, metadata

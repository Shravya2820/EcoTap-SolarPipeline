"""
fetcher.py
Main interface to fetch satellite images from different providers.
"""

from pathlib import Path
from .providers.google_static import GoogleStaticProvider
from .providers.esri import EsriProvider
from .cache import FetchCache


class ImageFetcher:
    def __init__(self, provider_name="esri", out_dir="data/raw", api_key=None):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

        self.cache = FetchCache(self.out_dir)

        # choose provider
        if provider_name == "google":
            self.provider = GoogleStaticProvider(api_key=api_key)
        elif provider_name == "esri":
            self.provider = EsriProvider()
        else:
            raise ValueError(f"Unknown provider: {provider_name}")

    def fetch(self, sample_id, lat, lon, zoom=20):
        """
        Returns (image_path, metadata)
        """

        # check cache
        cached = self.cache.get_cached(sample_id)
        if cached:
            return cached

        # fetch and save
        img_path, metadata = self.provider.fetch_image(sample_id, lat, lon, zoom)
        self.cache.save_cache(sample_id, img_path, metadata)

        return img_path, metadata

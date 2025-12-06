"""
Simple caching system to prevent re-downloading the same coordinates.
"""

import json
from pathlib import Path


class FetchCache:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _meta_path(self, sample_id):
        return self.base_dir / f"{sample_id}_meta.json"

    def _img_path(self, sample_id):
        return self.base_dir / f"{sample_id}.jpg"

    def get_cached(self, sample_id):
        meta_path = self._meta_path(sample_id)
        img_path = self._img_path(sample_id)

        if meta_path.exists() and img_path.exists():
            metadata = json.loads(meta_path.read_text())
            return img_path, metadata

        return None

    def save_cache(self, sample_id, img_path, metadata):
        # Save image
        target_img_path = self._img_path(sample_id)
        target_img_path.write_bytes(Path(img_path).read_bytes())

        # Save metadata
        meta_path = self._meta_path(sample_id)
        meta_path.write_text(json.dumps(metadata, indent=2))
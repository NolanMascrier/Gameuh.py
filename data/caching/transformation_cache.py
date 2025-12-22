"""For caching projectile transformations"""

from functools import lru_cache

class TransformCache:
    """Caches transformed versions of animations for reuse."""
    def __init__(self):
        self._cache = {}
        self._max_cache_size = 1024
        self._access_count = {}

    @lru_cache(1024)
    def get_key(self, image_name, rotation=0, scale=1.0, flip=False):
        """Generate cache key for transformation."""
        rotation = round(rotation / 5) * 5
        scale = round(scale, 2)
        return f"{image_name}|r{rotation}|s{scale}|f{flip}"

    def get(self, image_name, rotation=0, scale=1.0, flip=False):
        """Get cached transformed image or None."""
        key = self.get_key(image_name, rotation, scale, flip)
        if key in self._cache:
            self._access_count[key] = self._access_count.get(key, 0) + 1
            return self._cache[key]
        return None

    def put(self, image_name, transformed_image, rotation=0, scale=1.0, flip=False):
        """Store transformed image in cache."""
        key = self.get_key(image_name, rotation, scale, flip)
        if len(self._cache) >= self._max_cache_size:
            least_used = min(self._access_count.items(), key=lambda x: x[1])
            del self._cache[least_used[0]]
            del self._access_count[least_used[0]]

        self._cache[key] = transformed_image
        self._access_count[key] = 0

    def clear(self):
        """Clear the cache."""
        self._cache.clear()
        self._access_count.clear()

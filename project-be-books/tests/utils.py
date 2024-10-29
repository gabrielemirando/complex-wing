from django.core.cache import cache


class ClearCacheMixin:
    def tearDown(self):
        cache.clear()

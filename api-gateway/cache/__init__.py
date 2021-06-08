from flask_caching import Cache
from flask import Flask

cache: Cache = Cache(config={"CACHE_TYPE": "SimpleCache"})


def initialize_cache(app: Flask) -> None:
    cache.init_app(app)

from flask_caching import Cache

cache = Cache(config={"CACHE_TYPE": "SimpleCache"})


def initialize_cache(app):
    cache.init_app(app)

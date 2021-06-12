from flask import Flask
from flask_compress import Compress

compress: Compress = Compress()


def initialize_compress(app: Flask) -> None:
    compress.init_app(app)

from flask_mail import Mail
from flask import Flask

mailer: Mail = Mail()


def initialize_mailer(app: Flask) -> None:
    mailer.init_app(app)

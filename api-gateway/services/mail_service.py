from flask_mail import Message
from mailer import mailer
from middleware.error_handling import write_log


class MailService:
    @staticmethod
    def send_welcome_email(email: str, full_name: str) -> None:
        try:
            email = Message(
                subject="Welcome to DNSTool!",
                recipients=[email],
                body=f"Welcome {full_name} to DNSTool!",
            )
            mailer.send(email)
            return
        except Exception as e:
            write_log("error", e)

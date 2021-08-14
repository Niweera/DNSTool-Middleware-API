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

    @staticmethod
    def send_verification_email(email: str, verification_link: str) -> None:
        try:
            email = Message(
                subject="Verification Required!",
                recipients=[email],
                html=f"<h3>Please click on the following link to verify you</h3><br><a href='{verification_link}'>Click Here</a>",
            )
            mailer.send(email)
            return
        except Exception as e:
            write_log("error", e)

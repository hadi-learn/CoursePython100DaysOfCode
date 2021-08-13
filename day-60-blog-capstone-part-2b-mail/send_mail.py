import smtplib
import os

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
TARGET_MAIL = os.environ.get("TARGET_MAIL")


class SendMail:
    def __init__(self, username, email, phone, message):
        self.name = username
        self.email = email
        self.phone = phone
        self.message = message

    def send_email(self):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL, to_addrs=TARGET_MAIL,
                                msg=f"subject:User Message\n\n"
                                    f"User: {self.name}\n"
                                    f"Email: {self.email}\n"
                                    f"Phone: {self.phone}\n"
                                    f"Message: {self.message}")

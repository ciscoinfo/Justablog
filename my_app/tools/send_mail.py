import os
import smtplib
from dotenv import load_dotenv

load_dotenv()
SENDER_MAIL = os.environ.get('SENDER_MAIL', -1)
SENDER_PASS = os.environ.get('SENDER_PASS', -1)
TO_MAIL = os.environ.get('TO_MAIL', -1)

def send_email(subject, content):

    sender = {
        "email": SENDER_MAIL,
        "password": SENDER_PASS
    }

    mail_content = {
        "to": TO_MAIL,
        "subject": subject,
        "msg": content
    }

    _send_email(sender, mail_content)


def _send_email(sender, content):

    mail_server = "smtp.gmail.com"

    with smtplib.SMTP(mail_server, port=587) as connection:
        connection.starttls()
        connection.login(user=sender.get('email'), password=sender.get('password'))
        connection.sendmail(from_addr=sender.get('email'),
                            to_addrs=content.get("to"),
                            msg=f"Subject:{content.get('subject')}\n\n{content.get('msg')}".encode("utf8")
                            )

if __name__ == "__main__":

    send_email(subject="salut", content="Message de test")
    # print(SENDER_MAIL)
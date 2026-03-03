import smtplib
from email.message import EmailMessage

def send_alert(subject, content):
    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = subject
    msg["From"] = "monitor@m-motors.com"
    msg["To"] = "admin@m-motors.com"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("your_email", "your_password")
        server.send_message(msg)
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


def send_tracking_email(status: str, timestamp: str, tracking_id: str):
    """Sends an email notification via Brevo SMTP when a new update is found."""
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_login = os.getenv("SMTP_LOGIN")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender_email = os.getenv("SENDER_EMAIL")
    recipient_email = os.getenv("RECIPIENT_EMAIL")

    if not all([smtp_server, smtp_login, smtp_password, sender_email, recipient_email]):
        print("Error: Missing SMTP configuration in .env file.")
        return

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = f"📦 Ninja Van Tracking Update: {tracking_id}"

    body = f"""Hello,

A new tracking update was detected for your package ({tracking_id}):

• Status: {status}
• Date/Time: {timestamp}

View status online:
https://www.ninjavan.co/en-ph/international/tracking?id={tracking_id}

Best regards,
Automated Tracking Service
"""
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_login, smtp_password)
            server.send_message(msg)
        print(f"Notification email successfully sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
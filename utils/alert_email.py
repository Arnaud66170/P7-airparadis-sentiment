import os
import smtplib
from email.mime.text import MIMEText

def send_alert_email(nb_bad_feedbacks):
    try:
        smtp_server = os.getenv("EMAIL_HOST")
        port = int(os.getenv("EMAIL_PORT", 587))
        sender = os.getenv("EMAIL_HOST_USER")
        password = os.getenv("EMAIL_HOST_PASSWORD")
        receiver = os.getenv("EMAIL_RECEIVER")

        print("=== [GMAIL ALERT DEBUG] ===")
        print(f"SMTP Server     : {smtp_server}")
        print(f"Port            : {port}")
        print(f"Sender          : {sender}")
        print(f"Receiver        : {receiver}")
        print(f"Password present: {bool(password)}")

        if not all([smtp_server, port, sender, receiver, password]):
            print("❌ Erreur : une ou plusieurs variables d’environnement sont manquantes.")
            return

        subject = "🚨 Alerte : feedbacks négatifs détectés"
        body = f"⚠️ Attention : {nb_bad_feedbacks} feedbacks négatifs ont été signalés récemment sur l'application Air Paradis."

        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = receiver

        with smtplib.SMTP(smtp_server, port, timeout=10) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, message.as_string())

        print("✅ Email d’alerte envoyé avec succès.")

    except Exception as e:
        print("❌ Erreur lors de l’envoi d’email :", e)

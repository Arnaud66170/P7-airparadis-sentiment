import os
import smtplib
from email.message import EmailMessage

def send_alert_email(nb_bad_feedbacks):
    smtp_server = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    port = int(os.getenv("EMAIL_PORT", 587))
    sender = os.getenv("EMAIL_HOST_USER")
    receiver = os.getenv("EMAIL_RECEIVER")
    password = os.getenv("EMAIL_HOST_PASSWORD")

    print("=== [GMAIL ALERT DEBUG] ===")
    print("SMTP Server     :", smtp_server)
    print("Port            :", port)
    print("Sender          :", sender)
    print("Receiver        :", receiver)
    print("Password present:", bool(password))

    if not all([smtp_server, port, sender, receiver, password]):
        print("❌ Paramètres SMTP incomplets.")
        return

    subject = "⚠️ Alerte : Trop de feedbacks négatifs"
    body = f"Le système a détecté {nb_bad_feedbacks} feedbacks négatifs en moins de 5 minutes. 🚨"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            print("✅ Email d’alerte envoyé avec succès.")
    except Exception as e:
        print(f"❌ Erreur lors de l’envoi d’email : {e}")

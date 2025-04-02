import os
import smtplib
from email.mime.text import MIMEText

def send_alert_email(nb_bad_feedbacks):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender = os.getenv("GMAIL_SENDER")
    receiver = os.getenv("GMAIL_RECEIVER")
    password = os.getenv("GMAIL_PASSWORD")

    print("🧪 Secrets récupérés :")
    print("SMTP Server:", smtp_server)
    print("Port:", port)
    print("Sender:", sender)
    print("Receiver:", receiver)
    print("Password présent :", bool(password))

    if not all([smtp_server, port, sender, receiver, password]):
        print("❌ Erreur : une ou plusieurs variables d’environnement sont manquantes.")
        return

    subject = "🚨 Alerte feedbacks négatifs"
    body = f"⚠️ Il y a eu {nb_bad_feedbacks} feedbacks négatifs dans les 5 dernières minutes. À surveiller !"

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = receiver

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, message.as_string())
        print("✅ Email envoyé avec succès.")
    except Exception as e:
        print(f"❌ Erreur envoi email avec Gmail : {e}")

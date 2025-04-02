# utils/alert_email.py
import os
import smtplib
from email.message import EmailMessage

def send_alert_email(nb_bad_feedbacks):
    # Récupération des variables d'environnement
    smtp_server = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("EMAIL_PORT", 587))
    sender = os.getenv("EMAIL_HOST_USER")
    password = os.getenv("EMAIL_HOST_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    print("🧪 Secrets récupérés :")
    print("SMTP Server:", smtp_server)
    print("Port:", smtp_port)
    print("Sender:", sender)
    print("Receiver:", receiver)
    print("Password présent :", bool(password))

    # Vérification des variables
    if not all([smtp_server, smtp_port, sender, password, receiver]):
        print("❌ Erreur : une ou plusieurs variables d’environnement sont manquantes.")
        return

    # Création du message
    msg = EmailMessage()
    msg["Subject"] = "⚠️ Alerte : Feedbacks négatifs détectés"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content(f"{nb_bad_feedbacks} feedbacks négatifs ont été reçus en moins de 5 minutes.")

    # Envoi via SMTP sécurisé
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            print(f"✅ Mail envoyé à {receiver}")
    except Exception as e:
        print("❌ Erreur envoi email avec Gmail :", e)

import os
import smtplib
from email.mime.text import MIMEText

def send_alert_email(nb_bad_feedbacks):
    print("\n=== 📤 DÉMARRAGE ENVOI ALERT EMAIL ===")

    smtp_server = os.getenv("EMAIL_HOST")
    port = int(os.getenv("EMAIL_PORT", 587))
    sender = os.getenv("EMAIL_HOST_USER")
    password = os.getenv("EMAIL_HOST_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    # Log debug
    print(f"[DEBUG] SMTP Server     : {smtp_server}")
    print(f"[DEBUG] Port            : {port}")
    print(f"[DEBUG] Sender          : {sender}")
    print(f"[DEBUG] Receiver        : {receiver}")
    print(f"[DEBUG] Password present: {bool(password)}")

    if not all([smtp_server, port, sender, receiver, password]):
        print("❌ Une ou plusieurs variables d’environnement sont manquantes.")
        return

    subject = "🚨 Alerte : feedbacks négatifs détectés"
    body = f"Il y a eu {nb_bad_feedbacks} feedbacks négatifs dans les 5 dernières minutes. Veuillez vérifier les derniers tweets analysés."

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = receiver

    try:
        print("🔐 Connexion au serveur SMTP...")
        with smtplib.SMTP(smtp_server, port, timeout=10) as server:
            print("🔐 STARTTLS...")
            server.starttls()

            print("🔑 Connexion Gmail...")
            server.login(sender, password)

            print("📬 Envoi de l'email...")
            server.sendmail(sender, receiver, message.as_string())

        print("✅ Email envoyé avec succès.")
    except Exception as e:
        print(f"❌ Exception SMTP :", e)

    print("=== 📤 FIN ENVOI ALERT EMAIL ===\n")

# utils/alert_email.py

import requests

def send_alert_email(nb_bad_feedbacks):
    try:
        response = requests.post(
            "https://web-production-662f7.up.railway.app/send-alert",
            json={"nb_feedbacks": nb_bad_feedbacks}
        )
        print(f"✅ Appel API Railway : {response.status_code} | {response.json()}")
    except Exception as e:
        print(f"❌ Échec appel API d’alerte : {e}")



# import os
# import smtplib
# from email.mime.text import MIMEText

# def send_alert_email(nb_bad_feedbacks):
#     smtp_server = os.getenv("EMAIL_HOST")
#     port = int(os.getenv("EMAIL_PORT", 587))
#     sender = os.getenv("EMAIL_HOST_USER")
#     receiver = os.getenv("EMAIL_RECEIVER")
#     password = os.getenv("EMAIL_HOST_PASSWORD")

#     print("=== [GMAIL ALERT DEBUG] ===")
#     print("SMTP Server     :", smtp_server)
#     print("Port            :", port)
#     print("Sender          :", sender)
#     print("Receiver        :", receiver)
#     print("Password present:", bool(password))

#     if not all([smtp_server, port, sender, receiver, password]):
#         print("❌ Erreur : Une ou plusieurs variables d’environnement sont manquantes.")
#         return

#     message = MIMEText(f"🚨 Alerte automatique : {nb_bad_feedbacks} feedbacks négatifs reçus en moins de 5 minutes.")
#     message['Subject'] = "Alerte Feedback Négatif - Air Paradis"
#     message['From'] = sender
#     message['To'] = receiver

#     try:
#         with smtplib.SMTP(smtp_server, port) as server:
#             server.starttls()
#             server.login(sender, password)
#             server.send_message(message)
#         print("✅ Email d’alerte envoyé avec succès.")
#     except Exception as e:
#         print("❌ Erreur lors de l’envoi d’email :", e)

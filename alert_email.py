import os
import sendgrid
from sendgrid.helpers.mail import Mail
import traceback

def send_alert_email(nb_bad_feedbacks):
    sender = os.getenv("SENDGRID_SENDER")
    receiver = os.getenv("EMAIL_RECEIVER")
    api_key = os.getenv("SENDGRID_API_KEY")

    subject = "🚨 Air Paradis - Alerte Feedback Négatif"
    body = f"⚠️ Attention : {nb_bad_feedbacks} feedbacks négatifs ont été reçus sur les dernières minutes.\nVeuillez vérifier le modèle de prédiction."

    message = Mail(
        from_email=sender,
        to_emails=receiver,
        subject=subject,
        plain_text_content=body
    )

    try:
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        response = sg.send(message)
        print(f"✅ Email envoyé via SendGrid - Status code : {response.status_code}")
    except Exception as e:
        print("❌ Erreur lors de l'envoi de l'e-mail avec SendGrid :")
        traceback.print_exc()

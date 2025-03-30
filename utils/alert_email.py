import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_alert_email(nb_bad_feedbacks):
    api_key = os.getenv("SENDGRID_API_KEY")
    sender = os.getenv("SENDGRID_SENDER")
    receiver = os.getenv("SENDGRID_RECEIVER")
    template_id = os.getenv("SENDGRID_TEMPLATE_ID")

    if not all([api_key, sender, receiver, template_id]):
        print("❌ Erreur : une ou plusieurs variables d’environnement sont manquantes.")
        return

    message = Mail(
        from_email=sender,
        to_emails=receiver
    )
    message.template_id = template_id
    message.dynamic_template_data = {
        "nb_feedbacks": nb_bad_feedbacks
    }

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(f"✅ Mail envoyé ! Status code: {response.status_code}")
    except Exception as e:
        print("❌ Erreur envoi email avec SendGrid :", e)


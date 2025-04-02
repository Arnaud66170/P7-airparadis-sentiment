import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Ajout du path projet si besoin
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.alert_email import send_alert_email


@patch("utils.alert_email.SendGridAPIClient")
def test_send_alert_email_success(mock_sendgrid):
    # Mock des variables d'environnement
    os.environ["SENDGRID_API_KEY"] = "fake-key"
    os.environ["SENDGRID_SENDER"] = "test@example.com"
    os.environ["SENDGRID_RECEIVER"] = "client@example.com"
    os.environ["SENDGRID_TEMPLATE_ID"] = "fake-template"

    # Mock du comportement du client
    mock_client = MagicMock()
    mock_sendgrid.return_value = mock_client
    mock_client.send.return_value.status_code = 202

    send_alert_email(5)  # Ne doit pas planter

    mock_client.send.assert_called_once()


def test_send_alert_email_missing_env(monkeypatch):
    # Supprime les variables d'environnement
    monkeypatch.delenv("SENDGRID_API_KEY", raising=False)
    monkeypatch.delenv("SENDGRID_SENDER", raising=False)
    monkeypatch.delenv("SENDGRID_RECEIVER", raising=False)
    monkeypatch.delenv("SENDGRID_TEMPLATE_ID", raising=False)

    # Ne doit pas lever d’exception, mais afficher une erreur
    send_alert_email(3)

# lancement du test :
# pytest tests/test_alert_email.py
import sys
import os

# Ajout du path projet pour pouvoir importer huggingface_api.config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import requests
from huggingface_api.config import API_URL  # <- URL locale définie dans config.py

def test_local_prediction():
    payload = {
        "text": "This flight was absolutely horrible!"
    }

    response = requests.post(API_URL, json=payload)

    assert response.status_code == 200
    result = response.json()

    assert "label" in result
    assert result["label"] in [0, 1]
    assert "proba" in result


# commande gitbash test cloud :
# pytest tests/test_api_cloud.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import requests

def test_local_prediction():
    url = "http://127.0.0.1:8000/predict"

    payload = {
        "text": "This flight was absolutely horrible!"
    }

    response = requests.post(url, json=payload)

    assert response.status_code == 200
    result = response.json()

    # Vérifie les bonnes clés attendues dans la réponse
    expected_keys = ["label", "proba"]
    for key in expected_keys:
        assert key in result

    assert result["label"] in [0, 1]
    assert 0.0 <= result["proba"] <= 1.0



# commandes gitbash test local :
# uvicorn api:app --reload
# pytest tests/test_api_local.py
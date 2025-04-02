import sys
import os
import requests

# Ajout du dossier racine au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def test_local_prediction():
    url = "http://127.0.0.1:8000/predict"

    payload = {
        "text": "This flight was absolutely horrible!"
    }

    response = requests.post(url, json=payload)

    # Vérifie que l'API répond correctement
    assert response.status_code == 200

    result = response.json()

    # Vérifie la présence des clés attendues
    assert "label" in result
    assert "proba" in result

    # Vérifie les types et valeurs
    assert isinstance(result["label"], int)
    assert result["label"] in [0, 1]
    assert isinstance(result["proba"], float)
    assert 0.0 <= result["proba"] <= 1.0

    print("✅ Résultat local:", result)


# commandes gitbash test local :
# uvicorn api:app --reload
# pytest tests/test_api_local.py
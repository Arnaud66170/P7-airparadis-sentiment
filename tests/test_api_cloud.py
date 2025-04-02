import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import requests

def test_cloud_prediction():
    # URL du Hugging Face Space Gradio → endpoint /predict
    url = "https://arnaud66170--p7-airparadis-sentiment.hf.space/predict"

    payload = {
        "text": "I had an amazing experience with your airline!"
    }

    response = requests.post(url, json=payload)

    assert response.status_code == 200
    result = response.json()

    assert "prediction" in result
    assert result["prediction"] in [0, 1]


# commande gitbash test cloud :
# pytest tests/test_api_cloud.py

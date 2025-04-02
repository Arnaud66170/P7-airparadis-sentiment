import requests

def test_local_prediction():
    # URL locale (API FastAPI lancée via uvicorn)
    url = "http://127.0.0.1:8000/predict"

    payload = {
        "text": "This flight was absolutely horrible!"
    }

    response = requests.post(url, json=payload)

    assert response.status_code == 200
    result = response.json()

    assert "prediction" in result
    assert result["prediction"] in [0, 1]


# commandes gitbash test local :
# uvicorn api:app --reload
# pytest tests/test_api_local.py
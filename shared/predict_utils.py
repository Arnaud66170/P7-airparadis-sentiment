# === predict_utils.py ===
# Utilitaires partagés pour prédire avec LogReg + TF-IDF

import requests
import pandas as pd
from config import API_URL, LABELS, EMOJIS, COLORS

# === Fonction prédiction simple ===
def predict_single(text):
    try:
        response = requests.post(API_URL, json={"text": text})
        response.raise_for_status()
        data = response.json()
        label = data.get("label", 0)
        proba = round(data.get("proba", 0.0) * 100, 1)
        sentiment = LABELS[label]
        emoji = EMOJIS[label]
        color = COLORS[label]

        return {
            "text": text,
            "label": label,
            "sentiment": sentiment,
            "proba": proba,
            "emoji": emoji,
            "color": color
        }
    except Exception as e:
        print("[ERROR] predict_single:", e)
        return {
            "text": text,
            "label": -1,
            "sentiment": "Error",
            "proba": 0.0,
            "emoji": "❓",
            "color": "gray"
        }

# === Fonction prédiction par lot (liste de textes) ===
def predict_batch(text_list):
    results = []
    for text in text_list:
        prediction = predict_single(text)
        results.append(prediction)

    df = pd.DataFrame(results)
    df = df[["text", "sentiment", "proba", "emoji"]]
    df.columns = ["Tweet", "Sentiment", "Confidence", "Emoji"]
    return df

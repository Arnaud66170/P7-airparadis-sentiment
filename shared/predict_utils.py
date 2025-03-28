# === predict_utils.py ===
# Utilitaires partagés pour prédire avec LogReg + TF-IDF

# Prédiction locale sans appel API, pour Hugging Face Space

import pandas as pd
import joblib
import os
import re
import emoji
import spacy
from config import LABELS, EMOJIS, COLORS, MODEL_PATH, VECTORIZER_PATH

# === Chargement modèle et vectorizer ===
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# === Chargement spaCy ===
try:
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

# === Prétraitement du texte ===
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@[A-Za-z0-9_]+", "", text)
    text = emoji.replace_emoji(text, replace="")
    text = re.sub(r"[^a-zA-Z ]", "", text)
    text = ' '.join([word for word in text.split() if len(word) > 1])
    return text

def lemmatize_text(text):
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc if not token.is_stop])

def preprocess(text):
    text = clean_text(text)
    text = lemmatize_text(text)
    return text

# === Fonction prédiction simple ===
def predict_single(text):
    try:
        processed = preprocess(text)
        vectorized = vectorizer.transform([processed])
        prediction = model.predict(vectorized)[0]
        proba = round(model.predict_proba(vectorized)[0][prediction] * 100, 1)

        return {
            "text": text,
            "label": int(prediction),
            "sentiment": LABELS[prediction],
            "proba": proba,
            "emoji": EMOJIS[prediction],
            "color": COLORS[prediction]
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

# === Fonction prédiction par lot ===
def predict_batch(text_list):
    results = []
    for text in text_list:
        prediction = predict_single(text)
        results.append(prediction)

    df = pd.DataFrame(results)
    df = df[["text", "sentiment", "proba", "emoji"]]
    df.columns = ["Tweet", "Sentiment", "Confidence", "Emoji"]
    return df











# import requests
# import pandas as pd
# from config import API_URL, LABELS, EMOJIS, COLORS

# # === Fonction prédiction simple ===
# def predict_single(text):
#     try:
#         response = requests.post(API_URL, json={"text": text})
#         response.raise_for_status()
#         data = response.json()
#         label = data.get("label", 0)
#         proba = round(data.get("proba", 0.0) * 100, 1)
#         sentiment = LABELS[label]
#         emoji = EMOJIS[label]
#         color = COLORS[label]

#         return {
#             "text": text,
#             "label": label,
#             "sentiment": sentiment,
#             "proba": proba,
#             "emoji": emoji,
#             "color": color
#         }
#     except Exception as e:
#         print("[ERROR] predict_single:", e)
#         return {
#             "text": text,
#             "label": -1,
#             "sentiment": "Error",
#             "proba": 0.0,
#             "emoji": "❓",
#             "color": "gray"
#         }

# # === Fonction prédiction par lot (liste de textes) ===
# def predict_batch(text_list):
#     results = []
#     for text in text_list:
#         prediction = predict_single(text)
#         results.append(prediction)

#     df = pd.DataFrame(results)
#     df = df[["text", "sentiment", "proba", "emoji"]]
#     df.columns = ["Tweet", "Sentiment", "Confidence", "Emoji"]
#     return df

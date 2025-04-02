# === predict_utils.py ===
# Utilitaires partagés pour prédire avec LogReg + TF-IDF

import pandas as pd
import joblib
import re
import emoji
import spacy

try:
    # ✅ Local avec structure huggingface_api/
    from huggingface_api.config import LABELS, EMOJIS, COLORS, MODEL_PATH, VECTORIZER_PATH
except ModuleNotFoundError:
    # ✅ Hugging Face Space ou exécution depuis /app
    from config import LABELS, EMOJIS, COLORS, MODEL_PATH, VECTORIZER_PATH

# === Chargement du modèle et vectorizer ===
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# === Chargement du modèle spaCy (avec fallback automatique) ===
try:
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

# === Nettoyage texte ===
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@[A-Za-z0-9_]+", "", text)
    text = emoji.replace_emoji(text, replace="")
    text = re.sub(r"[^a-zA-Z ]", "", text)
    text = ' '.join([word for word in text.split() if len(word) > 1])
    return text

# === Lemmatisation ===
def lemmatize_text(text: str) -> str:
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc if not token.is_stop])

# === Pipeline complet de prétraitement ===
def preprocess(text: str) -> str:
    cleaned = clean_text(text)
    lemmatized = lemmatize_text(cleaned)
    return lemmatized

# === Prédiction unique ===
def predict_single(text: str) -> dict:
    try:
        processed = preprocess(text)
        vectorized = vectorizer.transform([processed])
        label = int(model.predict(vectorized)[0])
        proba = round(model.predict_proba(vectorized)[0][label] * 100, 1)

        return {
            "text": text,
            "label": label,
            "sentiment": LABELS[label],
            "proba": proba,
            "emoji": EMOJIS[label],
            "color": COLORS[label]
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

# === Prédiction par lot ===
def predict_batch(text_list: list) -> pd.DataFrame:
    results = [predict_single(text) for text in text_list]
    df = pd.DataFrame(results)
    return df[["text", "sentiment", "proba", "emoji"]].rename(
        columns={"text": "Tweet", "sentiment": "Sentiment", "proba": "Confidence", "emoji": "Emoji"}
    )

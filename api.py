from fastapi import FastAPI, Request
import joblib
import re
import emoji
import spacy
from pydantic import BaseModel

# ✅ Import dynamique pour compatibilité local + Hugging Face Space
try:
    from huggingface_api.config import MODEL_PATH, VECTORIZER_PATH, LABELS
except ModuleNotFoundError:
    from config import MODEL_PATH, VECTORIZER_PATH, LABELS

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

# === FastAPI ===
app = FastAPI()

class Tweet(BaseModel):
    text: str

@app.post("/predict")
def predict(tweet: Tweet):
    processed = preprocess(tweet.text)
    vectorized = vectorizer.transform([processed])
    prediction = model.predict(vectorized)[0]
    proba = model.predict_proba(vectorized)[0][prediction]

    sentiment = LABELS[prediction]  # Ajouté ici

    return {
        "label": int(prediction),
        "sentiment": sentiment,
        "proba": round(proba, 4)
    }

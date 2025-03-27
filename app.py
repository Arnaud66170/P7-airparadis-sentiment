import os
import joblib
import re
import emoji
import spacy
import gradio as gr

# === Chargement du modèle et du vectorizer ===
MODEL_PATH = "model/log_reg_model.pkl"
VECTORIZER_PATH = "model/tfidf_vectorizer.pkl"

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# === Chargement de spaCy ===
try:
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

# === Prétraitement du texte (même pipeline que l'entraînement) ===
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

# === Prédiction ===
def predict_sentiment(tweet):
    processed = preprocess(tweet)
    vectorized = vectorizer.transform([processed])
    prediction = model.predict(vectorized)[0]
    sentiment = "Positif 😊" if prediction == 1 else "Négatif 😡"
    return sentiment

# === Interface Gradio ===
with gr.Blocks(title="Analyse de Sentiment - Air Paradis") as demo:
    gr.Markdown("""
    # 📊 Prédiction de Sentiment Twitter - Air Paradis
    Entrez un tweet ci-dessous pour savoir s'il est perçu comme **positif** ou **négatif**.
    """)

    with gr.Row():
        with gr.Column():
            tweet_input = gr.Textbox(lines=3, placeholder="Entrez un tweet ici...", label="🔢 Tweet")
            predict_button = gr.Button("Prédire")
        with gr.Column():
            sentiment_output = gr.Textbox(label="🔀 Sentiment Prédit", interactive=False)

    predict_button.click(fn=predict_sentiment, inputs=tweet_input, outputs=sentiment_output)

# === Lancement local (optionnel) ===
if __name__ == "__main__":
    demo.launch()

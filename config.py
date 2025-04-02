# === config.py ===
# Configuration centrale du projet Gradio + API

import os

# === Chemin absolu vers le dossier huggingface_api/ (utile si lancé depuis la racine du projet)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 📁 Chemins vers les modèles (compatibles depuis n'importe où dans le projet)
MODEL_PATH = os.path.join(BASE_DIR, "model", "log_reg_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "model", "tfidf_vectorizer.pkl")

# 🌐 URL de l'API FastAPI locale
API_URL_LOCAL = "http://localhost:8000/predict"

# 🌐 URL de l'API Hugging Face (Gradio)
API_URL_HF = "https://arnaud66170--p7-airparadis-sentiment.hf.space/run/predict"

# ⚙️ Autres constantes
LABELS = {0: "Negative", 1: "Positive"}
EMOJIS = {0: "😡", 1: "😊"}
COLORS = {0: "red", 1: "green"}

# 📊 Pour l'analyse batch
DEFAULT_BATCH_COLUMN_NAMES = ["text", "tweet", "message"]

# 📝 Pour le fichier d'export
EXPORT_FILENAME = "batch_predictions.csv"
EXPORT_FOLDER = "data"  # dossier à créer si absent

# 🚨 Feedback alerts
FEEDBACK_ALERT_THRESHOLD = 3

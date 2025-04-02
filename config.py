# === config.py ===
# Configuration centrale du projet Gradio + API

import os

# === Chemin absolu vers le dossier huggingface_api/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 📁 Chemins vers les modèles (résoud dynamiquement le chemin absolu)
# MODEL_PATH = os.path.join(BASE_DIR, "model", "log_reg_model.pkl")
# VECTORIZER_PATH = os.path.join(BASE_DIR, "model", "tfidf_vectorizer.pkl")
MODEL_PATH = "huggingface_api/model/log_reg_model.pkl"
VECTORIZER_PATH = "huggingface_api/model/tfidf_vectorizer.pkl"

# 🌐 URL de l'API FastAPI
API_URL = "http://localhost:8000/predict"

# ⚙️ Autres constantes
LABELS = {0: "Negative", 1: "Positive"}
EMOJIS = {0: "😡", 1: "😊"}
COLORS = {0: "red", 1: "green"}

# Pour l'analyse batch
DEFAULT_BATCH_COLUMN_NAMES = ["text", "tweet", "message"]  # pour détection auto de colonne

# Pour le fichier d'export
EXPORT_FILENAME = "batch_predictions.csv"
EXPORT_FOLDER = "data"  # dossier à créer si absent

# Feedback alerts
FEEDBACK_ALERT_THRESHOLD = 3

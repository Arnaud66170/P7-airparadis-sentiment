import os
import shutil

# === Chemins source et destination ===
SOURCE_MODEL = "../models_saved/log_reg_model.pkl"
SOURCE_VECTORIZER = "../models_saved/tfidf_vectorizer.pkl"
DEST_DIR = "huggingface_clean/model/"

# === Création du dossier destination si besoin ===
os.makedirs(DEST_DIR, exist_ok=True)

# === Copie des fichiers ===
try:
    shutil.copy2(SOURCE_MODEL, os.path.join(DEST_DIR, "log_reg_model.pkl"))
    print("✅ Modèle LogReg copié avec succès.")
except FileNotFoundError:
    print("❌ Modèle LogReg introuvable !")

try:
    shutil.copy2(SOURCE_VECTORIZER, os.path.join(DEST_DIR, "tfidf_vectorizer.pkl"))
    print("✅ Vectorizer TF-IDF copié avec succès.")
except FileNotFoundError:
    print("❌ Vectorizer TF-IDF introuvable !")

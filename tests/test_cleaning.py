import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# from huggingface_api.shared.predict_utils import clean_text, lemmatize_text, preprocess
from shared.predict_utils import clean_text, lemmatize_text, preprocess


def test_clean_text_removes_url_and_mentions():
    text = "Check this: https://example.com and @AirParadis"
    cleaned = clean_text(text)
    assert "http" not in cleaned.lower()
    assert "@" not in cleaned

def test_clean_text_removes_emojis():
    text = "The flight was awful 😡😡"
    cleaned = clean_text(text)
    assert "😡" not in cleaned
    assert "awful" in cleaned

def test_lemmatize_text_basic():
    text = "The flights were delayed and passengers were shouting"
    lemmatized = lemmatize_text(text)
    # Vérifie que certains mots sont lemmatisés (selon le modèle spaCy)
    assert "flight" in lemmatized or "flights" not in lemmatized
    assert "be" not in lemmatized  # 'were' lemmatisé
    assert "shouting" not in lemmatized or "shout" in lemmatized

def test_preprocess_combines_clean_and_lemmatize():
    raw_text = "Awful service!! Check this: https://badurl.com 😡😡 @Airline"
    processed = preprocess(raw_text)
    assert "http" not in processed
    assert "😡" not in processed
    assert "awful" in processed or "service" in processed


# commande gitbash test nettoyage :
# pytest tests/test_cleaning.py

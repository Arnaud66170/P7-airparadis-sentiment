import sys
import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from huggingface_api.shared.predict_utils import predict_single
from shared.predict_utils import predict_single

def test_sanity_check():
    assert True

def test_predict_single_output_structure():
    result = predict_single("The flight was horrible")

    # Vérifie que la sortie est bien un dictionnaire
    assert isinstance(result, dict)

    # Vérifie la présence de toutes les clés attendues
    expected_keys = ["text", "label", "sentiment", "proba", "emoji", "color"]
    for key in expected_keys:
        assert key in result

def test_predict_single_prediction_validity():
    result = predict_single("Everything was perfect, I loved it!")

    # Vérifie que la prédiction est dans les classes possibles
    assert result["label"] in [0, 1]

    # Vérifie que le score de confiance est cohérent
    assert 0.0 <= result["proba"] <= 100.0

def test_predict_single_error_handling():
    # Donne volontairement une mauvaise entrée
    result = predict_single(None)

    assert result["label"] == -1
    assert result["sentiment"] == "Error"
    assert result["emoji"] == "❓"
    assert result["color"] == "gray"

if __name__ == "__main__":
    test_predict_single_output_structure()
    test_predict_single_prediction_validity()
    test_predict_single_error_handling()

# commande gitbash test prédiction :
# pytest -v tests/test_prediction.py --no-cov

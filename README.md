---
title: Air Paradis - Analyse de Sentiment
emoji: 🛫
colorFrom: gray
colorTo: blue
sdk: gradio
sdk_version: "3.44.4"
app_file: app.py
pinned: false
---

# 🧠 Air Paradis - Analyse de Sentiment Twitter

Bienvenue sur l'application **d'analyse de sentiment** développée pour la compagnie aérienne **Air Paradis**, dans le cadre du projet P7 du parcours Data Scientist - MLOps.

Cette application permet de prédire le **sentiment (positif ou négatif)** d’un tweet en lien avec la marque, afin d’anticiper les bad buzz potentiels sur les réseaux sociaux.

---

## 🎯 Objectifs du projet

- Mettre en œuvre un modèle de Machine Learning léger et performant
- Créer une interface simple d’utilisation pour des équipes non techniques
- Déployer le prototype via Hugging Face Spaces pour un accès rapide

---

## 🧩 Modèle retenu

- **Modèle** : Régression Logistique (Logistic Regression)
- **Vectorisation** : TF-IDF (Term Frequency - Inverse Document Frequency)
- **Prétraitement** : Nettoyage + lemmatisation avec spaCy
- **Entraînement** : sur un jeu de données de 1,5M de tweets nettoyés
- **Performances** :
  - Accuracy : ≈ 75.6%
  - F1-score : ≈ 76.4%

Ce modèle a été sélectionné pour son excellent **rapport performance/simplicité** et sa **compatibilité avec un déploiement rapide** sur des plateformes gratuites.

---

## 🛠️ Technologies utilisées

- **Langage** : Python 3
- **Machine Learning** : scikit-learn
- **Prétraitement NLP** : spaCy, regex, emoji
- **Interface utilisateur** : Gradio
- **Déploiement** : Hugging Face Spaces

---

## 🖥️ Utilisation de l’application

1. Renseignez un tweet dans le champ texte prévu à cet effet
2. Cliquez sur **"Prédire"**
3. L'application affiche si le sentiment est **positif** ou **négatif**

---

## 📌 Limites actuelles

- Analyse binaire uniquement (positif/négatif)
- Dataset généraliste (pas spécifique à Air Paradis)
- Pas de prise en compte du contexte temporel ou des tendances

---

## 🔭 Pistes d’amélioration

- Ajout d’une base de tweets réels mentionnant Air Paradis
- Intégration d’une option de feedback pour signaler les erreurs de prédiction
- Suivi dans le temps des évolutions de sentiment par période
- Passage à une architecture MLOps avec monitoring et réentraînement automatisé

---

## 📁 Fichiers présents

- `app.py` : Interface Gradio principale
- `model/` : Contient le modèle entraîné (`log_reg_model.pkl`) et le vectorizer (`tfidf_vectorizer.pkl`)
- `requirements.txt` : Dépendances pour Hugging Face Spaces

---

## 🧑‍💻 Auteur

Projet 7 réalisé par Arnaud CAILLE – Parcours AI Engineer – OpenClassrooms 2025


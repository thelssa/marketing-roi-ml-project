# 📈 Marketing ROI Optimizer

Projet de fin d’année visant à optimiser les investissements marketing grâce au Machine Learning, Deep Learning, FastAPI et Streamlit.

---

## Contexte

Les entreprises investissent dans plusieurs canaux marketing :

- TV
- Radio
- Social Media
- Influence marketing

Le problème est qu’il est difficile de savoir à l’avance si ces investissements seront rentables.

Ce projet permet de :

- prédire les ventes
- estimer le ROI
- comparer différents scénarios marketing
- aider à la prise de décision

---

## Objectif

Optimiser les budgets marketing afin de maximiser les ventes et le ROI.

---

## Architecture globale

Données brutes  
→ Data Engineering  
→ Dataset préparé  
→ Machine Learning / Deep Learning  
→ API FastAPI  
→ Dashboard Streamlit  
→ Décision marketing  

---

## Structure du projet

marketing-roi-ml-project/
- api/
- dashboard/
- data/
- models/
- notebooks/
- reports/
- src/
- requirements.txt
- README.md

---

## Machine Learning

Modèles testés :

- Linear Regression
- Random Forest
- Gradient Boosting
- XGBoost
- MLP Regressor

### Meilleur modèle

MLP Regressor

- RMSE : 2.56
- R² : 0.9992

### Modèle utilisé en production

Gradient Boosting

- RMSE : 3.91
- R² : 0.9982

---

## API FastAPI

Lancer :

uvicorn api.app:app --reload

Swagger :

http://127.0.0.1:8000/docs

Endpoints :

- GET /health
- POST /predict

---

## Dashboard Streamlit

Lancer :

streamlit run dashboard/app.py

Fonctionnalités :

- simulation de budget
- prédiction des ventes
- estimation du ROI
- recommandations automatiques
- comparaison de scénarios
- visualisations interactives

---

## Installation

git clone <repo_url>
cd marketing-roi-ml-project
python -m venv venv

Activation Windows :

venv\Scripts\activate

Installation dépendances :

pip install -r requirements.txt

---

## Stack technique

- Python
- Pandas
- Scikit-learn
- TensorFlow
- XGBoost
- FastAPI
- Streamlit
- Plotly
- SHAP

---

## Résultats Business

Le projet permet :

- d’optimiser les budgets marketing
- de prédire les ventes
- d’améliorer le ROI
- d’aider à la prise de décision

---

## Auteurs

Projet réalisé dans le cadre du Projet Data Science.

- Mai Dao → Data Engineering
- Thelma LUM → Machine Learning / Deep Learning
- Partie commune → API + Dashboard + rapport

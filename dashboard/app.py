from pathlib import Path
import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# Configuration générale

st.set_page_config(
    page_title="Marketing ROI Optimizer",
    page_icon="📈",
    layout="wide"
)


# Paths

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "marketing_clean.csv"

API_URL = "http://127.0.0.1:8000/predict"


# Chargement dataset

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()


# Header

st.title("📈 Marketing ROI Optimizer")

st.markdown("""
Ce dashboard permet à un responsable marketing de simuler différents scénarios 
budgétaires afin d’optimiser les ventes et le retour sur investissement.
""")


# KPIs globaux

st.header("📊 Indicateurs globaux")

col1, col2, col3 = st.columns(3)

col1.metric("Nombre de campagnes", len(df))
col2.metric("Ventes moyennes", round(df["sales"].mean(), 2))
col3.metric("ROI moyen", round(df["roi"].mean(), 2))

st.divider()


# Simulateur

st.header("🎯 Simulateur de campagne")

col1, col2 = st.columns(2)

with col1:
    tv = st.slider("Budget TV", 0, 300, 100)
    radio = st.slider("Budget Radio", 0, 100, 30)

with col2:
    social_media = st.slider("Budget Social Media", 0, 100, 20)
    
    influencer = st.selectbox(
        "Type d’influenceur",
        ["Macro", "Mega", "Micro", "Nano"]
    )


# Appel API

payload = {
    "tv": tv,
    "radio": radio,
    "social_media": social_media,
    "influencer": influencer
}

try:
    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        predicted_sales = result["predicted_sales"]
        estimated_roi = result["roi"]
    else:
        st.error("Erreur API")
        predicted_sales = 0
        estimated_roi = 0

except:
    st.error("Impossible de contacter l’API FastAPI.")
    predicted_sales = 0
    estimated_roi = 0


# Résultat principal

total_budget = tv + radio + social_media

st.header("📌 Résultat de la simulation")

col1, col2, col3 = st.columns(3)

col1.metric("Ventes prédites", round(predicted_sales, 2))
col2.metric("Budget total", total_budget)
col3.metric("ROI estimé", round(estimated_roi, 2))


# Recommandation automatique

st.divider()
st.header("💡 Recommandation marketing")

if estimated_roi >= 2.5:
    st.success("Excellente campagne : ROI élevé.")
elif estimated_roi >= 1.5:
    st.info("Campagne correcte : optimisation possible.")
else:
    st.warning("ROI faible : revoir la stratégie.")

if tv > radio and tv > social_media:
    st.write("📺 La télévision domine votre stratégie.")
elif radio > tv and radio > social_media:
    st.write("📻 La radio domine votre stratégie.")
else:
    st.write("📱 Le social media domine votre stratégie.")


# Comparaison scénarios

st.divider()
st.header("⚖️ Comparaison de scénarios")

scenario_payload = {
    "tv": tv + 20,
    "radio": radio,
    "social_media": social_media,
    "influencer": influencer
}

try:
    scenario_response = requests.post(API_URL, json=scenario_payload)

    if scenario_response.status_code == 200:
        scenario_result = scenario_response.json()
        prediction_tv_plus = scenario_result["predicted_sales"]
    else:
        prediction_tv_plus = 0

except:
    prediction_tv_plus = 0

comparison_df = pd.DataFrame({
    "Scénario": ["Actuel", "+20 Budget TV"],
    "Ventes prédites": [predicted_sales, prediction_tv_plus]
})

fig = px.bar(
    comparison_df,
    x="Scénario",
    y="Ventes prédites",
    text="Ventes prédites",
    title="Impact d’une augmentation du budget TV"
)

st.plotly_chart(fig, use_container_width=True)


# Importance variables

st.divider()
st.header("📌 Importance des variables")

importance_df = pd.DataFrame({
    "Variable": [
        "tv",
        "total_budget",
        "sales_per_tv",
        "tv_radio",
        "sales_per_radio"
    ],
    "Importance": [
        0.948367,
        0.045114,
        0.006467,
        0.000022,
        0.000009
    ]
})

fig2 = px.bar(
    importance_df,
    x="Importance",
    y="Variable",
    orientation="h",
    title="Variables les plus influentes"
)

st.plotly_chart(fig2, use_container_width=True)


# Analyse historique

st.divider()
st.header("📊 Analyse historique")

col1, col2 = st.columns(2)

with col1:
    fig3 = px.scatter(
        df,
        x="tv",
        y="sales",
        color="influencer",
        title="Relation TV vs Sales"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    fig4 = px.histogram(
        df,
        x="roi",
        nbins=30,
        title="Distribution du ROI"
    )
    st.plotly_chart(fig4, use_container_width=True)


# Dataset

st.divider()

with st.expander("Voir le dataset préparé"):
    st.dataframe(df.head(100))

# Données préparées

st.divider()
st.header("🗂️ Dataset préparé")

with st.expander("Afficher les données préparées"):
    st.dataframe(df)


# Conclusion métier

st.divider()

st.markdown("""
## 🧠 Conclusion métier

Ce dashboard transforme les modèles de Machine Learning en outil d’aide à la décision.

Il permet à une entreprise de :

- tester plusieurs stratégies marketing
- prédire les ventes
- analyser le ROI
- optimiser ses investissements publicitaires

L’objectif final est d’améliorer la performance commerciale.
""")

# uvicorn api.app:app --reload
# streamlit run dashboard/app.py
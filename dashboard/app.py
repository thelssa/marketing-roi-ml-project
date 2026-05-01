import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import plotly.express as px

# ---------------------------------------------------------
# Configuration générale du dashboard
# ---------------------------------------------------------
st.set_page_config(
    page_title="Marketing ROI Optimizer",
    page_icon="📈",
    layout="wide"
)

# ---------------------------------------------------------
# Chemins du projet
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "marketing_clean.csv"
MODEL_PATH = BASE_DIR / "models" / "best_model_gb.pkl"

# ---------------------------------------------------------
# Chargement des données et du modèle
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


df = load_data()
model = load_model()

# ---------------------------------------------------------
# En-tête
# ---------------------------------------------------------
st.title("📈 Marketing ROI Optimizer")

st.markdown(
    """
    Ce dashboard permet à un responsable marketing de simuler différents scénarios budgétaires,
    d’estimer les ventes attendues et d’analyser le retour sur investissement d’une campagne.
    """
)

# ---------------------------------------------------------
# KPIs globaux
# ---------------------------------------------------------
st.header("📊 Indicateurs globaux")

col1, col2, col3 = st.columns(3)

col1.metric("Nombre de campagnes", len(df))
col2.metric("Ventes moyennes", round(df["sales"].mean(), 2))
col3.metric("ROI moyen", round(df["roi"].mean(), 2))

st.divider()

# ---------------------------------------------------------
# Simulateur de campagne
# ---------------------------------------------------------
st.header("🎯 Simulateur de campagne")

col1, col2 = st.columns(2)

with col1:
    tv = st.slider("Budget TV", 0, 300, 100)
    radio = st.slider("Budget Radio", 0, 100, 30)

with col2:
    social = st.slider("Budget Social Media", 0, 100, 20)
    influencer = st.selectbox(
        "Type d’influenceur",
        ["Macro", "Mega", "Micro", "Nano"]
    )

# ---------------------------------------------------------
# Création des variables nécessaires au modèle
# ---------------------------------------------------------
total_budget = tv + radio + social

tv_share = tv / total_budget if total_budget > 0 else 0
radio_share = radio / total_budget if total_budget > 0 else 0
social_media_share = social / total_budget if total_budget > 0 else 0

input_data = pd.DataFrame([{
    "tv": tv,
    "radio": radio,
    "social_media": social,
    "total_budget": total_budget,
    "tv_share": tv_share,
    "radio_share": radio_share,
    "social_media_share": social_media_share,
    "tv_radio": tv * radio,
    "tv_social": tv * social,
    "radio_social": radio * social,
    "sales_per_tv": 0,
    "sales_per_radio": 0,
    "sales_per_social": 0,
    "influencer_Mega": 1 if influencer == "Mega" else 0,
    "influencer_Micro": 1 if influencer == "Micro" else 0,
    "influencer_Nano": 1 if influencer == "Nano" else 0
}])

# ---------------------------------------------------------
# Prédiction
# ---------------------------------------------------------
predicted_sales = model.predict(input_data)[0]
estimated_roi = predicted_sales / total_budget if total_budget > 0 else 0

st.header("📌 Résultat de la simulation")

col1, col2, col3 = st.columns(3)

col1.metric("Ventes prédites", round(predicted_sales, 2))
col2.metric("Budget total", round(total_budget, 2))
col3.metric("ROI estimé", round(estimated_roi, 2))

# ---------------------------------------------------------
# Recommandation automatique
# ---------------------------------------------------------
st.divider()
st.header("💡 Recommandation marketing")

if total_budget == 0:
    st.warning("Veuillez saisir un budget supérieur à zéro pour obtenir une recommandation.")
elif estimated_roi >= 2.5:
    st.success("Excellente campagne : le ROI estimé est élevé. La stratégie budgétaire semble pertinente.")
elif estimated_roi >= 1.5:
    st.info("Campagne correcte : le ROI est positif, mais une optimisation des canaux peut améliorer la performance.")
else:
    st.warning("ROI faible : il est recommandé de revoir la répartition des budgets avant lancement.")

if tv >= radio and tv >= social:
    st.write("📺 Le budget TV est le levier dominant dans ce scénario.")
elif radio >= tv and radio >= social:
    st.write("📻 Le budget Radio est le levier dominant dans ce scénario.")
else:
    st.write("📱 Le budget Social Media est le levier dominant dans ce scénario.")

# ---------------------------------------------------------
# Comparaison de scénarios
# ---------------------------------------------------------
st.divider()
st.header("⚖️ Comparaison de scénarios")

scenario_tv_plus = input_data.copy()
scenario_tv_plus["tv"] = scenario_tv_plus["tv"] + 20
scenario_tv_plus["total_budget"] = (
    scenario_tv_plus["tv"]
    + scenario_tv_plus["radio"]
    + scenario_tv_plus["social_media"]
)
scenario_tv_plus["tv_share"] = scenario_tv_plus["tv"] / scenario_tv_plus["total_budget"]
scenario_tv_plus["radio_share"] = scenario_tv_plus["radio"] / scenario_tv_plus["total_budget"]
scenario_tv_plus["social_media_share"] = scenario_tv_plus["social_media"] / scenario_tv_plus["total_budget"]
scenario_tv_plus["tv_radio"] = scenario_tv_plus["tv"] * scenario_tv_plus["radio"]
scenario_tv_plus["tv_social"] = scenario_tv_plus["tv"] * scenario_tv_plus["social_media"]
scenario_tv_plus["radio_social"] = scenario_tv_plus["radio"] * scenario_tv_plus["social_media"]

prediction_tv_plus = model.predict(scenario_tv_plus)[0]

comparison_df = pd.DataFrame({
    "Scénario": ["Budget actuel", "+20 budget TV"],
    "Ventes prédites": [predicted_sales, prediction_tv_plus]
})

fig_comparison = px.bar(
    comparison_df,
    x="Scénario",
    y="Ventes prédites",
    text="Ventes prédites",
    title="Comparaison des ventes prédites selon le scénario"
)

st.plotly_chart(fig_comparison, use_container_width=True)

st.write(
    f"Dans ce scénario, une augmentation de 20 unités du budget TV ferait passer les ventes prédites "
    f"de **{round(predicted_sales, 2)}** à **{round(prediction_tv_plus, 2)}**."
)

# ---------------------------------------------------------
# Importance des variables
# ---------------------------------------------------------
st.divider()
st.header("📌 Importance des variables")

importance_df = pd.DataFrame({
    "Variable": input_data.columns,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

fig_importance = px.bar(
    importance_df.head(10),
    x="Importance",
    y="Variable",
    orientation="h",
    title="Top 10 des variables les plus influentes"
)

st.plotly_chart(fig_importance, use_container_width=True)

st.markdown(
    """
    L’analyse de l’importance des variables permet de comprendre quels leviers influencent
    le plus les prédictions du modèle. Dans ce projet, le budget TV ressort comme le facteur
    le plus déterminant dans la prédiction des ventes.
    """
)

# ---------------------------------------------------------
# Visualisations exploratoires utiles au décideur
# ---------------------------------------------------------
st.divider()
st.header("📊 Analyse des campagnes existantes")

col1, col2 = st.columns(2)

with col1:
    fig_sales_tv = px.scatter(
        df,
        x="tv",
        y="sales",
        color="influencer",
        title="Relation entre budget TV et ventes"
    )
    st.plotly_chart(fig_sales_tv, use_container_width=True)

with col2:
    fig_roi = px.histogram(
        df,
        x="roi",
        nbins=30,
        title="Distribution du ROI des campagnes"
    )
    st.plotly_chart(fig_roi, use_container_width=True)

# ---------------------------------------------------------
# Données
# ---------------------------------------------------------
st.divider()
st.header("🗂️ Dataset préparé")

with st.expander("Afficher les données préparées"):
    st.dataframe(df)

# ---------------------------------------------------------
# Conclusion métier
# ---------------------------------------------------------
st.divider()
st.markdown(
    """
    ### 🧠 Lecture métier

    Ce dashboard transforme le modèle de machine learning en outil décisionnel.
    Il permet à un responsable marketing de tester des hypothèses budgétaires,
    d’obtenir une estimation des ventes et d’identifier les leviers les plus influents.

    L’objectif final est d’aider à mieux répartir les investissements marketing afin
    de maximiser la performance commerciale et le ROI.
    """
)

#streamlit run dashboard/app.py
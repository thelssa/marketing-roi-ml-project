import joblib
from pathlib import Path

# ---------------------------------------------------------
# Charger le modèle sauvegardé
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "best_model_gb.pkl"

model = joblib.load(MODEL_PATH)
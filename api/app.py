from fastapi import FastAPI
import pandas as pd

from api.model_loader import model
from api.schema import MarketingInput

app = FastAPI(
    title="Marketing ROI API",
    description="API de prédiction marketing",
    version="1.0"
)


# Health check
@app.get("/health")
def health():
    return {
        "status": "ok"
    }



# Prediction endpoint
@app.post("/predict")
def predict(data: MarketingInput):

    total_budget = data.tv + data.radio + data.social_media

    tv_share = data.tv / total_budget if total_budget else 0
    radio_share = data.radio / total_budget if total_budget else 0
    social_share = data.social_media / total_budget if total_budget else 0

    input_data = pd.DataFrame([{
        "tv": data.tv,
        "radio": data.radio,
        "social_media": data.social_media,
        "total_budget": total_budget,
        "tv_share": tv_share,
        "radio_share": radio_share,
        "social_media_share": social_share,
        "tv_radio": data.tv * data.radio,
        "tv_social": data.tv * data.social_media,
        "radio_social": data.radio * data.social_media,
        "sales_per_tv": 0,
        "sales_per_radio": 0,
        "sales_per_social": 0,
        "influencer_Mega": 1 if data.influencer == "Mega" else 0,
        "influencer_Micro": 1 if data.influencer == "Micro" else 0,
        "influencer_Nano": 1 if data.influencer == "Nano" else 0
    }])

    prediction = model.predict(input_data)[0]

    roi = prediction / total_budget if total_budget else 0

    return {
        "predicted_sales": round(float(prediction), 2),
        "roi": round(float(roi), 2)
    }

# Model info endpoint 
@app.get("/model-info")
def model_info():
    return {
        "model_name": "Gradient Boosting Regressor",
        "purpose": "Sales prediction + ROI optimization"
    }

# uvicorn api.app:app --reload
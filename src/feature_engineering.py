import pandas as pd
import numpy as np


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Sécurité : éviter division par zéro
    total_budget = df["tv"] + df["radio"] + df["social_media"]
    total_budget = total_budget.replace(0, np.nan)

    # 1. Budget total
    df["total_budget"] = df["tv"] + df["radio"] + df["social_media"]

    # 2. Parts de budget
    df["tv_share"] = df["tv"] / total_budget
    df["radio_share"] = df["radio"] / total_budget
    df["social_media_share"] = df["social_media"] / total_budget

    # 3. ROI / proxy marketing
    df["roi"] = df["sales"] / total_budget

    # 4. Interactions entre canaux
    df["tv_radio"] = df["tv"] * df["radio"]
    df["tv_social"] = df["tv"] * df["social_media"]
    df["radio_social"] = df["radio"] * df["social_media"]

    # 5. Ratios utiles
    df["sales_per_tv"] = df["sales"] / df["tv"].replace(0, np.nan)
    df["sales_per_radio"] = df["sales"] / df["radio"].replace(0, np.nan)
    df["sales_per_social"] = df["sales"] / df["social_media"].replace(0, np.nan)

    # 6. Encodage simple du type d’influenceur:
    if "influencer" in df.columns:
        influencer_dummies = pd.get_dummies(df["influencer"], prefix="influencer", drop_first=True)
        df = pd.concat([df, influencer_dummies], axis=1)

    # Remplir les NaN créés par divisions par zéro
    ratio_cols = [
        "tv_share", "radio_share", "social_media_share",
        "roi", "sales_per_tv", "sales_per_radio", "sales_per_social"
    ]
    for col in ratio_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    return df
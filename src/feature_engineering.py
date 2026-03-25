import pandas as pd
import numpy as np


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Calcul du budget total (somme des canaux)
    total_budget = df[["tv", "radio", "social_media"]].sum(axis=1)
    total_budget = total_budget.replace(0, np.nan)

    # Ajout du budget total au dataset
    df["total_budget"] = total_budget

    # Calcul de la contribution de chaque canal dans le budget global
    df["tv_share"] = df["tv"] / total_budget
    df["radio_share"] = df["radio"] / total_budget
    df["social_media_share"] = df["social_media"] / total_budget

    # Calcul du ROI (retour sur investissement marketing)
    df["roi"] = df["sales"] / total_budget

    # Création de variables d’interaction entre canaux marketing
    df["tv_radio"] = df["tv"] * df["radio"]
    df["tv_social"] = df["tv"] * df["social_media"]
    df["radio_social"] = df["radio"] * df["social_media"]

    # Ratios de performance par canal (efficacité individuelle)
    df["sales_per_tv"] = df["sales"] / df["tv"].replace(0, np.nan)
    df["sales_per_radio"] = df["sales"] / df["radio"].replace(0, np.nan)
    df["sales_per_social"] = df["sales"] / df["social_media"].replace(0, np.nan)

    # Encodage one-hot de la variable catégorielle "influencer" si elle existe
    if "influencer" in df.columns:
        influencer_dummies = pd.get_dummies(df["influencer"], prefix="influencer", drop_first=True)
        df = pd.concat([df, influencer_dummies], axis=1)

    # Remplacement des NaN issus des divisions par zéro
    ratio_cols = [
        "tv_share", "radio_share", "social_media_share",
        "roi", "sales_per_tv", "sales_per_radio", "sales_per_social"
    ]
    df[ratio_cols] = df[ratio_cols].fillna(0)

    return df
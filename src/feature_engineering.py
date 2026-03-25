import pandas as pd

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["total_budget"] = df["tv"] + df["radio"] + df["social_media"]
    df["tv_share"] = df["tv"] / df["total_budget"]
    df["radio_share"] = df["radio"] / df["total_budget"]
    df["social_media_share"] = df["social_media"] / df["total_budget"]
    df["roi_proxy"] = df["sales"] / df["total_budget"]
    df["tv_radio_interaction"] = df["tv"] * df["radio"]
    df["tv_social_interaction"] = df["tv"] * df["social_media"]
    return df
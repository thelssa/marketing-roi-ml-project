import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Normalisation des noms de colonnes (lowercase, sans espaces)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    return df


def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Remplissage des variables numériques par la médiane
    numeric_cols = ["tv", "radio", "social_media", "sales"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    # Remplissage des variables catégorielles par la modalité la plus fréquente
    if "influencer" in df.columns:
        df["influencer"] = df["influencer"].fillna(df["influencer"].mode()[0])

    return df
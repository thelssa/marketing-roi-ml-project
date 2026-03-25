import pandas as pd

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ["tv", "radio", "social_media", "sales"]:
        df[col] = df[col].fillna(df[col].median())
    df["influencer"] = df["influencer"].fillna(df["influencer"].mode()[0])
    return df
from pathlib import Path
import pandas as pd

from src.preprocessing import clean_column_names, fill_missing_values
from src.feature_engineering import add_features


def load_data(path: str) -> pd.DataFrame:
    if path.endswith(".csv"):
        return pd.read_csv(path)
    elif path.endswith(".xlsx"):
        return pd.read_excel(path)
    else:
        raise ValueError("Format de fichier non supporté. Utilise un fichier .csv ou .xlsx")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_column_names(df)
    df = fill_missing_values(df)
    return df


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_data(df)
    df = add_features(df)
    return df

def save_data(df: pd.DataFrame, path: str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")


def main():
    input_path = "data/marketing_and_sales.csv"
    output_path = "data/processed/marketing_clean.csv"

    df = load_data(input_path)
    df_prepared = prepare_data(df)
    save_data(df_prepared, output_path)

    print(f"Fichier généré avec succès : {output_path}")
    print(df_prepared.head())


if __name__ == "__main__":
    main()
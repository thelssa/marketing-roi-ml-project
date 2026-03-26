import pandas as pd
from sklearn.model_selection import train_test_split

from src.preprocessing import clean_column_names, fill_missing_values
from src.feature_engineering import add_features


def load_data(path: str) -> pd.DataFrame:

    if path.endswith(".csv"):
        return pd.read_csv(path)
    elif path.endswith(".xlsx"):
        return pd.read_excel(path)
    else:
        raise ValueError("Format de fichier non supporté. Utilise un fichier .csv ou .xlsx")


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:

    df = clean_column_names(df)
    df = fill_missing_values(df)
    df = add_features(df)

    if "influencer" in df.columns:
        df = pd.get_dummies(df, columns=["influencer"], drop_first=True)

    return df


def split_data(
    df: pd.DataFrame,
    target: str = "sales",
    test_size: float = 0.2,
    random_state: int = 42
):

    if target not in df.columns:
        raise ValueError(f"La colonne cible '{target}' est absente du DataFrame.")

    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    return X_train, X_test, y_train, y_test


def save_data(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)
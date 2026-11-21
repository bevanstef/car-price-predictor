"""
train.py - Model Training & Evaluation Pipeline

Clean Architecture Step:
- Loads cleaned data (`cars_clean.csv`)
- Prepares feature matrix X and target y (`price_lkr`)
- Constructs scikit-learn preprocessing ColumnTransformer (OneHotEncoder + PassThrough)
- Evaluates models (Linear Regression baseline vs Random Forest Regressor)
- Persists best pipeline to `model.joblib`
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


def load_data(filepath: str = "cars_clean.csv"):
    """Load cleaned dataset and split into features (X) and target (y)."""
    df = pd.read_csv(filepath)
    X = df.drop(columns=["price_lkr"])
    y = df["price_lkr"]
    return X, y


def build_preprocessor():
    """Create ColumnTransformer for categorical one-hot encoding and numeric passthrough."""
    categorical_features = ["brand", "model", "fuel", "transmission"]
    numeric_features = ["year", "mileage_km", "engine_cc"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", "passthrough", numeric_features),
        ]
    )
    return preprocessor


def train_and_evaluate(X_train, X_test, y_train, y_test, preprocessor):
    """Train models, compare metrics, and return best pipeline."""
    # TODO: Implement step-by-step
    pass


def main():
    print("--- Starting Model Training ---")
    # TODO: Run pipeline and save model.joblib
    pass


if __name__ == "__main__":
    main()

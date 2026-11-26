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
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, random_state=42),
    }

    best_pipeline = None
    best_r2 = -float("inf")
    best_name = None

    print(f"\nTraining set size: {len(X_train)}, Test set size: {len(X_test)}\n")

    for name, model in models.items():
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("regressor", model),
        ])

        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)

        print(f"--- {name} ---")
        print(f"R² Score: {r2:.4f}")
        print(f"MAE: LKR {mae:,.2f}\n")

        if r2 > best_r2:
            best_r2 = r2
            best_pipeline = pipeline
            best_name = name

    print(f"Selected Best Model: {best_name} (R² = {best_r2:.4f})")
    return best_pipeline


def main():
    print("--- Starting Model Training Pipeline ---")
    X, y = load_data()
    print(f"Loaded dataset: {X.shape[0]} samples, {X.shape[1]} features")

    # 80/20 train/test split with reproducibility seed
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    preprocessor = build_preprocessor()
    best_pipeline = train_and_evaluate(X_train, X_test, y_train, y_test, preprocessor)

    # Persist the trained model pipeline to disk
    output_model_path = "model.joblib"
    joblib.dump(best_pipeline, output_model_path)
    print(f"[OK] Best pipeline saved to {output_model_path}")


if __name__ == "__main__":
    main()

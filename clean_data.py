"""
clean_data.py - Data Cleaning Pipeline for Used Car Dataset

Clean Architecture Step:
- Reads raw messy dataset (`cars_raw.csv`)
- Executes discrete, modular cleaning steps:
  1. Fix brand text casing
  2. Drop duplicate rows
  3. Impute or handle missing values
  4. Filter out impossible planted outliers
- Saves reproducible clean dataset (`cars_clean.csv`)
"""

import pandas as pd
import numpy as np


def load_raw_data(filepath: str = "cars_raw.csv") -> pd.DataFrame:
    """Load the raw messy dataset from disk."""
    return pd.read_csv(filepath)


def fix_brand_casing(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize brand names to Title Case (e.g., 'HONDA' -> 'Honda')."""
    df = df.copy()
    df["brand"] = df["brand"].str.title()
    print(f"Unique brands after casing fix: {df['brand'].nunique()} (expected: 8)")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop exact duplicate records."""
    before = len(df)
    df = df.drop_duplicates()
    dropped = before - len(df)
    print(f"Dropped {dropped} duplicate rows (remaining: {len(df)})")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values for mileage_km (by year median) and fuel (by model mode)."""
    df = df.copy()
    mileage_missing = df["mileage_km"].isna().sum()
    fuel_missing = df["fuel"].isna().sum()

    # 1. Impute mileage_km using the median mileage of cars from the same manufacturing year
    year_median_mileage = df.groupby("year")["mileage_km"].transform("median")
    df["mileage_km"] = df["mileage_km"].fillna(year_median_mileage).fillna(df["mileage_km"].median())

    # 2. Impute fuel using the most frequent (mode) fuel type for each car model
    model_mode_fuel = df.groupby("model")["fuel"].apply(
        lambda s: s.mode().iloc[0] if not s.mode().empty else "Petrol"
    )
    df["fuel"] = df["fuel"].fillna(df["model"].map(model_mode_fuel))

    print(f"Imputed missing values: {mileage_missing} mileage rows & {fuel_missing} fuel rows")
    return df


def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Remove corrupt planted outliers (e.g. 50,000 price & 950,000 km mileage)."""
    df = df.copy()
    initial_len = len(df)
    df = df[(df["price_lkr"] != 50000) & (df["mileage_km"] != 950000)]
    removed = initial_len - len(df)
    print(f"Removed {removed} planted outlier rows (remaining: {len(df)})")
    return df


def save_cleaned_data(df: pd.DataFrame, output_path: str = "cars_clean.csv") -> None:
    """Save the cleaned dataframe to CSV."""
    df.to_csv(output_path, index=False)
    print(f"[OK] Cleaned dataset saved to {output_path}")


def main():
    print("--- Starting Data Cleaning Pipeline ---")
    df_raw = load_raw_data()
    print(f"Raw shape: {df_raw.shape}")

    # Pipeline execution flow
    df_clean = (
        df_raw
        .pipe(fix_brand_casing)
        .pipe(remove_duplicates)
        .pipe(handle_missing_values)
        .pipe(remove_outliers)
    )

    print(f"Cleaned shape: {df_clean.shape}")
    save_cleaned_data(df_clean)


if __name__ == "__main__":
    main()

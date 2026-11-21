import pandas as pd

df = pd.read_csv("cars_raw.csv")

print("Shape(raws, column) : ", df.shape)
print("\n Column data types : ", df.dtypes)
print("\n Missing vlaues per column : ", df.isna().sum())
print("\n Duplicates rows:", df.duplicated().sum())
print("\n Brand counts (Look for different spellings): \n", df["brand"].value_counts())

def iqr_outliers(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    low = q1 - 1.5 * iqr
    high = q3 + 1.5 * iqr
    return series[(series < low) | (series > high)], low, high

for col in ["price_lkr", "mileage_km"]:
    outliers, low, high = iqr_outliers(df[col])
    print(f"\n{col}: normal range {low:,.0f} to {high:,.0f}, flagged {len(outliers)} rows")
    print(df.loc[outliers.index, ["brand", "model", "year", "mileage_km", "price_lkr"]].sort_values(col).head(10))
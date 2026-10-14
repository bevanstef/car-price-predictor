import pandas as pd

df = pd.read_csv("cars_raw.csv")

print("Shape(raws, column) : ", df.shape)
print("\n Column data types : ", df.dtypes)
print("\n Missing vlaues per column : ", df.isna().sum())
print("\n Duplicates rows:", df.duplicated().sum())
print("\n Brand counts (Look for different spellings): \n", df["brand"].value_counts())


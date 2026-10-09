import pandas as pd

df = pd.read_csv("cars_raw.csv")

print("Shape(raws, column) : ", df.shape)
print("\n Column data types : ", df.dtypes)
print("\n Missing vlaues per column : ", df.isna().sum())


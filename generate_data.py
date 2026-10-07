import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 3000

# brand: base price in LKR millions for a fairly new car
brands = {
    "Toyota": 9.0, "Suzuki": 6.0, "Honda": 8.5, "Nissan": 7.5,
    "Mitsubishi": 8.0, "Micro": 4.5, "Kia": 7.0, "Perodua": 4.0,
}

# each brand's common models, with a price multiplier relative to that brand's base price
models = {
    "Toyota": {"Aqua": 1.0, "Prius": 1.3, "Corolla": 1.1, "Vitz": 0.8, "Axio": 1.0},
    "Suzuki": {"Alto": 0.7, "Wagon R": 0.85, "Swift": 1.0, "Every": 0.9},
    "Honda": {"Fit": 0.9, "Vezel": 1.35, "Civic": 1.2, "Grace": 1.05},
    "Nissan": {"Leaf": 1.2, "Sunny": 0.9, "X-Trail": 1.4, "March": 0.75},
    "Mitsubishi": {"Montero": 1.5, "Lancer": 1.0, "Mirage": 0.75},
    "Micro": {"Panda": 0.8, "Geely": 0.9},
    "Kia": {"Picanto": 0.8, "Rio": 0.95, "Sportage": 1.3},
    "Perodua": {"Axia": 0.75, "Bezza": 0.9},
}

fuels = ["Petrol", "Diesel", "Hybrid", "Electric"]
gears = ["Manual", "Automatic"]

brand = rng.choice(list(brands), N)
model = [rng.choice(list(models[b])) for b in brand]     # pick a model that belongs to that brand
model_mult = np.array([models[b][m] for b, m in zip(brand, model)])

year = rng.integers(2005, 2025, N)
age = 2025 - year
mileage = np.clip(age * rng.normal(11000, 3500, N), 1000, 300000).astype(int)
fuel = rng.choice(fuels, N, p=[0.55, 0.2, 0.2, 0.05])
gear = rng.choice(gears, N, p=[0.35, 0.65])
engine_cc = rng.choice([660, 800, 1000, 1300, 1500, 1800, 2000], N)

base = np.array([brands[b] for b in brand]) * model_mult    # model now affects price
price = base * (0.93 ** age)
price *= 1 - (mileage / 600000)
price *= 1 + (engine_cc - 1000) / 6000
price *= np.where(gear == "Automatic", 1.10, 1.0)
price *= np.select([fuel == "Hybrid", fuel == "Electric", fuel == "Diesel"], [1.15, 1.25, 1.05], 1.0)
price *= rng.normal(1, 0.06, N)
price = (price * 1_000_000).round(-4)

print("Sample:", brand[0], model[0], "-> Rs", price[0])

# Combine everything into one table
df = pd.DataFrame({
    "brand": brand,
    "model": model,
    "year": year,
    "mileage_km": mileage,
    "fuel": fuel,
    "transmission": gear,
    "engine_cc": engine_cc,
    "price_lkr": price,
})

# mess up dataset

# 1. Inconsistent text: randomly mess up casing on some brand names
messy_idx = rng.choice(df.index, 150, replace=False)
df.loc[messy_idx, "brand"] = df.loc[messy_idx, "brand"].str.upper()

# 2. Missing values: blank out some mileage and fuel entries
df.loc[rng.choice(df.index, 80, replace=False), "mileage_km"] = np.nan
df.loc[rng.choice(df.index, 50, replace=False), "fuel"] = np.nan

# 3. Outliers: a few unrealistic prices and mileages
df.loc[rng.choice(df.index, 10, replace=False), "price_lkr"] = 50000
df.loc[rng.choice(df.index, 10, replace=False), "mileage_km"] = 950000

# 4. Duplicate rows
dupes = df.sample(30, random_state=1)
df = pd.concat([df, dupes], ignore_index=True)

# Shuffle rows so planted issues aren't grouped together
df = df.sample(frac=1, random_state=2).reset_index(drop=True)

df.to_csv("cars_raw.csv", index=False)
print(f"Saved {len(df)} rows (with intentional mess) to cars_raw.csv")
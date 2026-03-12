import pandas as pd

# Charger le dataset
df = pd.read_csv("anime_dataset.csv")

# Traiter les données
df["episodes"] = df["episodes"].round().astype("Int64")

# Suppression des données sans score
df = df.dropna(subset="score")

# Suppression des doublons
df = df.drop_duplicates()

df["episodes"] = df["episodes"].fillna(0)

print(df.dtypes)
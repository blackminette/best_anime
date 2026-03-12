import pandas as pd

# Charger le dataset
df = pd.read_csv("anime_dataset.csv")

# Traiter les données
print("NaN par colonne :")
print(df.isnull().sum())
print("\nDoublons :", df.duplicated().sum())

df["score"] = df["score"].fillna(round(df["score"].mean(), 2))

print(df.head(20))

print(df.dtypes)
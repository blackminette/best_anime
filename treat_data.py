import pandas as pd

# Charger le dataset
df = pd.read_csv("anime_dataset.csv")

# Traiter les données
print("NaN par colonne :")
print(df.isnull().sum())
print("\nDoublons :", df.duplicated().sum())

# Remplissage des valeurs vide de la colone score par la moyenne de la colonne
df["score"] = df["score"].fillna(round(df["score"].mean(), 2))

# Changement des types des colonnes episodes et year pour des Int64
df[["episodes", "year"]] = df[["episodes", "year"]].astype("Int64")

print(df[["title", "score", "episodes"]].head(20))

print(df.dtypes)
import pandas as pd
from flask import Flask, render_template
import ast
import numpy as np

# Charger le dataset
df = pd.read_csv("anime_dataset.csv")

# Nettoyer les données
df["episodes"] = df["episodes"].round().astype("Int64")

# Suppression des données sans score
df = df.dropna(subset="score")

# Suppression des doublons
df = df.drop_duplicates()

df["episodes"] = df["episodes"].fillna(0)

df["genres"] = df["genres"].apply(ast.literal_eval)
df["demographics"] = df["demographics"].apply(ast.literal_eval)
df["studios"] = df["studios"].apply(ast.literal_eval)

df["scored_by"] = df["scored_by"].round().astype(int)


# Bonus pour le calcul du score finale
conditions = [
    df["score"] >= 9,
    (df["score"] < 9) & (df["score"] >= 8),
    (df["score"] < 8) & (df["score"] >= 5)
]

choices = [50, 10, 5]

df["bonus_score_multiplier"] = np.select(conditions, choices, default=1)


# Score finale
df["score_final"] = (
    0.4 * df["score"] * df["bonus_score_multiplier"] + 
    0.25 * (df["scored_by"] / 10000) +
    0.25 * df["favorites"] / 100 +
    0.1 * df["members"] / 100000
    )

df["score_final"] = round(df["score_final"], 2)

df = df.sort_values("score_final", ascending=False)

# ==== Rendu html =====
condition = (
    (df["demographics"].apply(lambda x: "Seinen" in x))
    )

colonne = ["score_final", "title", "score", "scored_by", "members", "favorites", "episodes", "genres", "demographics", "studios"]

app = Flask(__name__)
@app.route("/")
def accueil():
    table = df.loc[:, colonne].head(10).to_html(index=False)
    return render_template("index.html", table=table)
app.run(debug=True)
import pandas as pd
from flask import Flask, render_template
import ast

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

print(df.dtypes)

# ==== Rendu html =====
app = Flask(__name__)
@app.route("/")
def accueil():
    table = df[["title", "score", "scored_by", "members", "favorites", "episodes", "genres", "demographics", "studios"]].head(10).to_html(index=False)
    return render_template("index.html", table=table)
app.run(debug=True)
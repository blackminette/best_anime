# Anime Dataset Analysis

## Contexte
Avant de commencer ce TP, j’ai désactivé **Copilot** dans VSCode afin de ne pas avoir d’auto-complétion automatique pendant le développement.

Lorsque j’ai entendu le sujet, ma première idée a été d’utiliser le site [MyAnimeList](https://myanimelist.net), car il possède une gigantesque base de données publique d’animes, probablement l’une des plus grandes.

Malheureusement, le site ne propose pas directement de dataset complet téléchargeable. J’ai donc demandé à une IA si c’était possible de récupérer les données et comment procéder. Au fur et à mesure de mes recherches, plusieurs solutions sont apparues :

* Utiliser un ou plusieurs datasets disponibles sur **Kaggle**
* Utiliser l’**API de MyAnimeList** pour créer mon propre dataset

J’ai finalement choisi la deuxième solution.

---

## Installation

### Cloner le projet
```bash
git clone <url_du_repo>
cd <nom_du_projet>
Installer les dépendances Python
Bash
```

```bash
pip install pandas numpy flask
Générer le dataset (si nécessaire)
Bash
```

```bash
python get_dataset.py
Lancer l'application
Bash
```
```python
python app.py
Ouvrir le navigateur à l'adresse : http://127.0.0.1:5000
```

# Création du dataset
Pour récupérer les données, j’ai écrit (avec l’aide de l’IA pour la requête API) un script get_dataset.py utilisant l’API Jikan, qui est une API non officielle permettant d’accéder aux données de MyAnimeList.

Après avoir exploré les premières données récupérées, j’ai modifié le script généré par l’IA afin :

De récupérer également le status de l’anime

De faciliter le traitement de la colonne episodes

De ne pas récupérer les entrées sans studio

J’avais initialement prévu d’utiliser l’année de sortie, mais j’ai finalement décidé de ne pas l’inclure car il manquait trop de données pour que cela soit exploitable. J’ai fait une dernière modification du script afin d’obtenir un dataset de base propre. Après cela, je n’ai plus modifié le script de récupération.

## Données conservées dans le dataset
Les colonnes conservées sont :

* id : indispensable pour pouvoir comparer avec d’autres datasets

* title : permet d’identifier l’anime

* score : note moyenne donnée par les utilisateurs de MyAnimeList

* scored_by : nombre total de votes pour cet anime

* members : nombre de membres dans la communauté de l’anime

* favorites : nombre d’utilisateurs ayant mis l’anime en favori

* episodes : nombre total d’épisodes (0 si pas commencé, None si en cours)

* genres : permet de comparer les animes par genre

* demographics : public cible de l’anime

* studios : studio d’animation

* status : permet de savoir si l’anime est terminé, en cours ou pas encore commencé

# Nettoyage des données
Plusieurs opérations de nettoyage ont été effectuées :

Conversion du type de la colonne episodes de float vers int64

Suppression des entrées sans score pour éviter de biaiser les résultats

Suppression des doublons

Python

df["episodes"] = df["episodes"].round().astype("Int64")
df = df.dropna(subset="score")
df = df.drop_duplicates()
df["episodes"] = df["episodes"].fillna(0)
## Transformation de certaines colonnes
Les colonnes genres, demographics et studios étaient stockées sous forme de chaînes de caractères représentant des listes. J’ai utilisé la bibliothèque ast avec la fonction literal_eval pour effectuer la conversion.

Python

df["genres"] = df["genres"].apply(ast.literal_eval)
df["demographics"] = df["demographics"].apply(ast.literal_eval)
df["studios"] = df["studios"].apply(ast.literal_eval)
## Calcul d’un score personnalisé
J’ai voulu créer un score final pour classer les animes. Mon idée était de donner beaucoup d’importance à la note moyenne (score), tout en prenant en compte d’autres indicateurs de popularité.

Comme certaines valeurs (members, favorites, etc.) peuvent être très grandes, j’ai décidé d’appliquer un bonus multiplicateur basé sur la note via NumPy (np.select) pour gérer les colonnes Pandas.

Python

conditions = [
    df["score"] >= 9,
    (df["score"] < 9) & (df["score"] >= 8),
    (df["score"] < 8) & (df["score"] >= 5)
]

choices = [50, 10, 5]

df["bonus_score_multiplier"] = np.select(conditions, choices, default=1)
## Formule du score final
Le score final est calculé de la manière suivante :

* 40 % : note moyenne avec multiplicateur

* 25 % : nombre de votes (scored_by)

* 25 % : nombre de favoris

* 10 % : nombre de membres

Python

df["score_final"] = (
    0.4 * df["score"] * df["bonus_score_multiplier"] + 
    0.25 * (df["scored_by"] / 10000) +
    0.25 * df["favorites"] / 100 +
    0.1 * df["members"] / 100000
)
# Affichage des résultats
J’ai choisi Flask pour afficher les résultats, car cela permet de séparer le code Python du template HTML et du CSS (généré avec l'aide de l'IA).

## Filtrage et rendu HTML
Le script permet également d’appliquer des conditions de filtrage grâce à df.loc. Exemple pour le public Seinen :

Python

condition = (
    (df["demographics"].apply(lambda x: "Seinen" in x))
)
Les 10 premiers animes selon le score final sont ensuite affichés dans une table HTML.

Python

table = df.loc[:, colonne].head(10).to_html(index=False)
# Technologies utilisées
Python

Pandas

NumPy

Flask

AST
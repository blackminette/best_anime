import requests
import pandas as pd
import time

base_url = "https://api.jikan.moe/v4"
anime_data = []

max_pages = 1500

for page in range(1, max_pages + 1):
    try:
        r = requests.get(f"{base_url}/anime?page={page}&limit=25")
        result = r.json()
    except Exception as e:
        print(f"Erreur page {page}: {e}")
        continue

    if "data" not in result or not result["data"]:
        break

    for anime in result["data"]:
        aid = anime["mal_id"]
        status = anime.get("status")
        studios = [s["name"] for s in anime.get("studios", [])]
        if not studios:
            continue

        if status == "Finished":
            episodes = anime["episodes"]
        elif status == "Airing":
            episodes = None
        elif status == "Upcoming":
            episodes = 0
        else:
            episodes = anime["episodes"]

        anime_data.append({
            "anime_id": aid,
            "title": anime["title"],
            "score": anime["score"],
            "scored_by": anime.get("scored_by"),
            "members": anime["members"],
            "favorites": anime["favorites"],
            "episodes": episodes,
            "genres": [g["name"] for g in anime.get("genres", [])],
            "demographics": [d["name"] for d in anime.get("demographics", [])],
            "studios": studios,
            "status": status
        })

    print(f"Page {page} récupérée, anime total jusqu'ici: {len(anime_data)}")
    time.sleep(0.8)  # plus rapide mais safe

df = pd.DataFrame(anime_data)
df.to_csv("anime_dataset.csv", index=False)
print("Datasets enregistrés ! Anime total :", len(anime_data))
import requests
import pandas as pd
import time

base_url = "https://api.jikan.moe/v4"
anime_data = []
character_data = []

max_pages = 300

for page in range(1, max_pages + 1):
    print(f"Récupération de la page {page}")
    r = requests.get(f"{base_url}/anime?page={page}&limit=25")
    result = r.json()
    
    if "data" not in result or not result["data"]:
        break

    for anime in result["data"]:
        aid = anime["mal_id"]
        status = anime.get("status")  # "Finished", "Airing", "Upcoming"
        studios = ", ".join([s["name"] for s in anime.get("studios", [])])

        if status == "Finished":
            episodes = anime["episodes"]
        elif status == "Airing":
            episodes = None  # ou "in progress"
        elif status == "Upcoming":
            episodes = 0  # ou "not aired yet"
        else:
            episodes = anime["episodes"]

        if not studios:
            continue
    
        anime_data.append({
            "anime_id": aid,
            "title": anime["title"],
            "score": anime["score"],
            "type": anime["type"],
            "episodes": anime["episodes"],
            "year": anime.get("year"),
            "genres": ", ".join([g["name"] for g in anime.get("genres", [])]),
            "studios": studios,
            "status": status
        })

    time.sleep(1)  # éviter le rate limit

print("Anime total récupérés :", len(anime_data))

df = pd.DataFrame(anime_data)

df.to_csv("anime_dataset.csv", index=False)

print("Datasets enregistrés !")
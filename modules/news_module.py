import requests
import os

API_KEY = os.getenv("NEWS_KEY")
URL = "https://newsapi.org/v2/top-headlines"

def fetch_news(country="mx", limit=5):
    params = {
        "apiKey": API_KEY,
        "country": country,
        "pageSize": limit
    }

    try:
        response = requests.get(URL, params=params)

        if response.status_code != 200:
            return []

        data = response.json()

        news_list = []
        for article in data["articles"]:
            title = article["title"]
            url = article["url"]
            summary = article["description"] or "Sin descripción"

            news_list.append({
                "title": title,
                "summary": summary,
                "url": url
            })

        return news_list
    
    except:
        return []

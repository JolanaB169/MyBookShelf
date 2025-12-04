import requests

def search_books(query):
    """
    Searches for books using Google Books API.
    Returns a list of parsed book dictionaries.
    """
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": query, "maxResults": 10}

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    data = response.json()

    results = []
    for item in data.get("items", []):
        volume = item.get("volumeInfo", {})

        results.append({
            "title": volume.get("title"),
            "authors": volume.get("authors", []),
            "description": volume.get("description"),
            "thumbnail": volume.get("imageLinks", {}).get("thumbnail"),
            "published_year": volume.get("publishedDate", "")[:4],
            "isbn": volume.get("industryIdentifiers", [{}])[0].get("identifier", "")
        })

    return results

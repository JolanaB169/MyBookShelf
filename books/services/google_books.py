import requests

# Base URL for the Google Books API
GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"

def search_google_books(query, max_results=10):
    """
        Search for books on Google Books using a query string.

        Args:
            query (str): The search term (e.g., book title or author name).
            max_results (int): Maximum number of results to return (default: 10, max 40 according to the API).

        Returns:
            list: A list of books, where each book is a dictionary containing information from the Google Books API.

        Raises:
            requests.HTTPError: If the API request fails (e.g., network error or invalid response).
        """
    params = {"q": query, "maxResults": max_results}
    r = requests.get(GOOGLE_BOOKS_URL, params=params)
    r.raise_for_status() # Raise exception for HTTP errors
    return r.json().get("items", [])

def get_google_book(volume_id):
    """
       Retrieve detailed information about a single book using its volume ID.

       Args:
           volume_id (str): The unique ID of the book from the Google Books API.

       Returns:
           dict: A dictionary containing detailed information about the book.

       Raises:
           requests.HTTPError: If the API request fails.
       """
    url = f"{GOOGLE_BOOKS_URL}/{volume_id}"
    r = requests.get(url)
    r.raise_for_status() # Raise exception for HTTP errors
    return r.json()
from books.models.books import Book
from books.models.authors import Author
from books.services.google_books import get_google_book


def extract_isbn(info):
    identifiers = info.get("industryIdentifiers", [])
    for item in identifiers:
        if item.get("type") in ["ISBN_13", "ISBN_10"]:
            return item.get("identifier")
    return None


def extract_year(info):
    date = info.get("publishedDate")
    if not date:
        return None

    # formats: "1998", "1998-01-01"
    return int(date.split("-")[0])


def import_book_from_google(volume_id):
    data = get_google_book(volume_id)
    info = data.get("volumeInfo", {})

    title = (info.get("title") or "Untitled")[:300]
    description = info.get("description") or "No description available."
    isbn_list = info.get("industryIdentifiers", [])
    isbn = None
    for id_item in isbn_list:
        if id_item.get("type") == "ISBN_13":
            isbn = id_item.get("identifier")
            break
    publisher = (info.get("publisher") or "")[:200]
    year = None
    if info.get("publishedDate"):
        try:
            year = int(info["publishedDate"][:4])
        except ValueError:
            year = None
    thumbnail = info.get("imageLinks", {}).get("thumbnail")
    google_id = volume_id[:200]

    book = Book.objects.create(
        title=title,
        description=description,
        isbn=isbn,
        publisher=publisher,
        year=year,
        thumbnail=thumbnail,
        google_id=google_id,
    )

    # Authors
    for author_name in info.get("authors", []):
        first, *last = author_name.split(" ", 1)
        last_name = last[0] if last else ""
        author_obj, _ = Author.objects.get_or_create(first_name=first, last_name=last_name)
        book.authors.add(author_obj)

    return book
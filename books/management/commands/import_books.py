import csv
from django.core.management.base import BaseCommand
from books.models import Book, Author

class Command(BaseCommand):
    help = "Import knih z CSV do hlavní databáze"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Cesta k CSV souboru s knihami")

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]
        count_books = 0
        count_authors = 0

        with open(csv_file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Autoři
                author_names = [a.strip() for a in row.get("authors", "").split(",") if a.strip()]
                authors_objs = []
                for name in author_names:
                    parts = name.split(" ", 1)
                    first_name = parts[0]
                    last_name = parts[1] if len(parts) > 1 else ""

                    # zpracování volitelných polí Author
                    year_of_birth = int(row.get("year_of_birth")) if row.get("year_of_birth") else 1900
                    year_of_death = int(row.get("year_of_death")) if row.get("year_of_death") else None
                    country = row.get("country") or None
                    biography = row.get("biography") or ""

                    author_obj, created = Author.objects.get_or_create(
                        first_name=first_name,
                        last_name=last_name,
                        defaults={
                            "year_of_birth": year_of_birth,
                            "year_of_death": year_of_death,
                            "country": country,
                            "biography": biography,
                        }
                    )
                    if created:
                        count_authors += 1
                    authors_objs.append(author_obj)

                # Kniha
                book, created = Book.objects.get_or_create(
                    title=row.get("title") or "Untitled",
                    defaults={
                        "isbn": row.get("isbn") or None,
                        "publisher": row.get("publisher") or None,
                        "year": int(row["year"]) if row.get("year") else None,
                        "description": row.get("description") or "",
                        "thumbnail": row.get("thumbnail") or None,
                    }
                )
                if created:
                    count_books += 1
                    book.authors.set(authors_objs)

        self.stdout.write(self.style.SUCCESS(
            f"Import dokončen: {count_books} knih, {count_authors} nových autorů."
        ))

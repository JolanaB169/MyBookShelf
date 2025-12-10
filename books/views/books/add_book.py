from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from books.forms import BookForm
from books.models.books import Author

@login_required
def add_book_view(request):
    """
    Allows a logged-in user to add a new book.
    Users can also add new authors inline.
    All books are automatically approved upon creation.
    """
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            book = form.save(commit=False)

            # Handle new authors
            new_authors_text = form.cleaned_data.get('new_authors', '')
            new_author_objs = []
            for line in new_authors_text.splitlines():
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                first_name = parts[0]
                last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
                author, created = Author.objects.get_or_create(first_name=first_name, last_name=last_name)
                new_author_objs.append(author)

            # Assign creator and approve book automatically
            book.created_by = request.user
            book.approved = True
            book.save()
            form.save_m2m()  # save ManyToMany fields like genre

            # Add authors (existing + new)
            existing_authors = form.cleaned_data.get('existing_authors')
            if existing_authors:
                book.authors.set(list(existing_authors) + new_author_objs)
            else:
                book.authors.set(new_author_objs)

            messages.success(request, "Kniha byla úspěšně přidána.")
            return redirect("book_list")
    else:
        form = BookForm()

    return render(request, "books/add_book.html", {"form": form})

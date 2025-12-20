from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from books.forms import AuthorForm
from books.models.books import Author

@login_required
def edit_author_view(request, author_id):
    """
    Allow logged-in users to edit author details.
    """
    author = get_object_or_404(Author, id=author_id)

    if request.method == "POST":
        form = AuthorForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            return redirect("author_detail", pk=author.pk)
    else:
        form = AuthorForm(instance=author)

    return render(request, "authors/edit_author.html", {"form": form, "author": author})

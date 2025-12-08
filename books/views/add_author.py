from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import AuthorForm



@login_required
def add_author_view(request):
    """
    Allows a logged-in user to add a new author.
    """
    if request.method == "POST":
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Autor byl úspěšně přidán.")
            return redirect("book_list")
    else:
        form = AuthorForm()

    return render(request, "add_author.html", {"form": form})

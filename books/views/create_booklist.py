from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import BookListForm

@login_required
def create_booklist(request):
    """
    Allow a logged-in user to create a new book list.
    """
    if request.method == "POST":
        form = BookListForm(request.POST)
        if form.is_valid():
            booklist = form.save(commit=False)
            booklist.owner = request.user
            booklist.save()
            messages.success(request, "Seznam byl vytvořen.")
            return redirect("profile")  # user lists page
    else:
        form = BookListForm()

    return render(request, "create_booklist.html", {"form": form})

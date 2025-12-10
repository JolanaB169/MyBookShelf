from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from books.models import Author

@login_required
def favorite_author(request, author_id):
    """
    Toggle an author as a favorite for the currently logged-in user.

    If the author is already in the user's preferred_authors, remove them.
    Otherwise, add the author to preferred_authors.

    Redirects back to the author's detail page after updating.
    """
    author = get_object_or_404(Author, id=author_id)
    profile = request.user.profile

    if author in profile.preferred_authors.all():
        profile.preferred_authors.remove(author)
    else:
        profile.preferred_authors.add(author)

    return redirect('author_detail', author_name=f"{author.first_name} {author.last_name}")

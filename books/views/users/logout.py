from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):
    """
    Logs out the current user and redirects to the homepage.
    """
    logout(request)
    return redirect("home_page")

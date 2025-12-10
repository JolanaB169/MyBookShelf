from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def login_view(request):
    """
    Handles user login: authenticates credentials and logs in the user,
    redirecting to the homepage on success or showing an error on failure.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile")
        else:
            messages.error(request, "Neplatné jméno nebo heslo")
    return render(request, "users/login.html")

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Hesla se neshodují")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Uživatel s tímto jménem již existuje")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Vítej, {username}! Jsi nyní přihlášen(a).")
                return redirect("home_page")

    return render(request, "register.html")


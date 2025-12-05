from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import UserProfile
from ..forms import UserProfileForm

@login_required
def profile_view(request):
    """
    Display and edit the currently logged-in user's profile.
    """
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "profile.html", {"profile": profile, "form": form})

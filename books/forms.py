from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    Form for updating the user's profile information.
    Allows the user to upload a profile photo and set a yearly reading goal.
    """
    class Meta:
        model = UserProfile
        fields = ["photo", "reading_goal"]
        widgets = {
            "favorite_genres": forms.CheckboxSelectMultiple(),
            "preferred_authors": forms.CheckboxSelectMultiple(),
        }
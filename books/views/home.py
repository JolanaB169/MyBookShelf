from django.shortcuts import render

def home_page(request):
    """View for rendering the homepage."""
    return render(request, 'main.html')
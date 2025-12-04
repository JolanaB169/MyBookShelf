from django.shortcuts import render

def home_page(request):
    """
    View for rendering the homepage.

    Args:
        request (HttpRequest): The Django request object.

    Returns:
        HttpResponse: Renders the main.html template as the homepage.
    """
    return render(request, 'main.html')
from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

def home(request):
    user_count = User.objects.count()
    context = {
        'user_count': user_count
    }
    return render(request, "core/home.html", context)

def about_us(request):
    """Render the About Us page."""
    return render(request, "core/AboutUs.html")

def how_it_works(request):
    """Render the How It Works page."""
    return render(request, "core/HowItWorks.html")

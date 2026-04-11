from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model

from .forms import RegisterForm, LoginForm
from .models import Profile
from .models import Lesson,Module,Course


User = get_user_model()


def home(request):
    user_count = User.objects.count()
    context = {
        'user_count': user_count
    }
    # template lives under accounts/templates/accounts/home.html
    return render(request, "accounts/home.html", context)


def about_us(request):
    """Render the About Us page."""
    # the template lives under the accounts app's templates folder
    return render(request, "accounts/AboutUs.html")


def how_it_works(request):
    """Render the How It Works page."""
    # the template lives under the accounts app's templates folder
    return render(request, "accounts/HowItWorks.html")


def auth(request):
    """Handle GET and POST for login and registration.

    The template uses `action=register` and `action=login` to distinguish forms.
    """
    next_url = request.GET.get('next', '')
    # default forms
    register_form = RegisterForm()
    login_form = LoginForm()
    show_signup = False

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'register':
            form = RegisterForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']

                # use email as username
                username = email
                user = User.objects.create_user(username=username, email=email, password=password,
                                                first_name=first_name, last_name=last_name)
                # Profile is created by signal, but ensure exists
                Profile.objects.get_or_create(user=user)

                login(request, user)
                messages.success(request, 'Account created and signed in.')
                return redirect(next_url or 'home')
            else:
                register_form = form
                show_signup = True

        elif action == 'login':
            form = LoginForm(request.POST)
            if form.is_valid():
                identifier = form.cleaned_data['username']
                password = form.cleaned_data['password']

                # Try authenticating by username first
                user = authenticate(request, username=identifier, password=password)
                if user is None:
                    # try by email
                    try:
                        u = User.objects.get(email__iexact=identifier)
                        user = authenticate(request, username=u.username, password=password)
                    except User.DoesNotExist:
                        user = None

                if user is not None:
                    login(request, user)
                    # messages.success(request, 'Signed in successfully.')
                    return redirect(next_url or 'home')
                else:
                    messages.error(request, 'Invalid credentials')
                    login_form = form
            else:
                login_form = form

    context = {
        'register_form': register_form,
        'form': login_form,
        'next': next_url,
        'show_signup': show_signup,
    }
    return render(request, 'accounts/auth.html', context)


def check_email(request):
    """AJAX endpoint to see if an email is already registered."""
    email = request.GET.get('email', '').strip()
    exists = False
    if email:
        exists = User.objects.filter(email__iexact=email).exists()
    return JsonResponse({'exists': exists})


def logout_view(request):
    logout(request)
    # messages.info(request, 'You have been signed out.')
    return redirect('home')

def word_course(request):
    # Fetch modules and prefetch their lessons to keep it fast
    modules = Module.objects.filter(course__name="Microsoft Word").prefetch_related('lessons')
    return render(request, 'accounts/word.html', {'modules': modules})

def excel_course(request):
    # Fetch modules and prefetch their lessons to keep it fast
    modules = Module.objects.filter(course__name="Microsoft Excel").prefetch_related('lessons')
    return render(request, 'accounts/excel.html', {'modules': modules})

def powerpoint_course(request):
    # Fetch modules and prefetch their lessons to keep it fast
    modules = Module.objects.filter(course__name="Microsoft PowerPoint").prefetch_related('lessons')
    return render(request, 'accounts/powerpoint.html', {'modules': modules})
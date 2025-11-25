from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import LinkCategory
from django.conf import settings


def public_page(request):
    categories = LinkCategory.objects.prefetch_related('links').all()
    
    # Filter links based on authentication
    for category in categories:
        if not request.user.is_authenticated:
            # For non-authenticated users, exclude authenticated_only links
            category.filtered_links = category.links.filter(authenticated_only=False)
        else:
            # For authenticated users, show all links
            category.filtered_links = category.links.all()
    
    context = {
        'categories': categories,
        'site_title': settings.SITE_TITLE,
        'site_subtitle': settings.SITE_SUBTITLE,
        'navbar_brand': settings.NAVBAR_BRAND,
        'footer_text': settings.FOOTER_TEXT,
        'meta_description': settings.META_DESCRIPTION,
        'meta_keywords': settings.META_KEYWORDS,
    }
    return render(request, 'links/public_page.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('public_page')
        messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'links/login.html', {'form': form})

# uncomment this view to allow self registration
"""def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('public_page')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'links/register.html', {'form': form})"""

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('public_page')
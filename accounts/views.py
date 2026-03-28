from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .models import Subscription


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            plan = form.cleaned_data.get('plan')
            Subscription.objects.create(
            user=user,
            plan=plan,
            is_active=False
    )
    return redirect('register_success')
    # redirect to a success page instead of showing a message

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # authenticate: checks username and password against database

        if user is not None:
            login(request, user)
            # login: creates a session for the user
            return redirect('vip')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    # logout: destroys the user session
    return redirect('homepage')


@login_required
# login_required: redirects to login page if user is not logged in
def vip(request):
    try:
        subscription = request.user.subscription
        # access subscription through OneToOneField relation

        if not subscription.is_valid():
            # subscription exists but is expired or inactive
            return render(request, 'accounts/subscription_expired.html')

    except Subscription.DoesNotExist:
        # user has no subscription at all
        return render(request, 'accounts/no_subscription.html')

    return render(request, 'accounts/vip.html', {
        'subscription': subscription,
        'today_year': __import__('datetime').date.today().year
    })
    
def register_success(request):
    return render(request, 'accounts/register_success.html', {
        'today_year': __import__('datetime').date.today().year
    })
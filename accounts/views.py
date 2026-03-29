from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import RegisterForm
from .models import Subscription
from bookings.models import VIPCode



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
            # ✅ indented correctly inside if form.is_valid()
            # only redirects AFTER successful form submission
    else:
        form = RegisterForm()
        # ✅ else: creates empty form for GET requests
        # this was missing! without it the form variable
        # doesn't exist when page is first visited

    return render(request, 'accounts/register.html', {'form': form})
    # ✅ renders the registration form for GET requests
    # and for POST requests where form is invalid

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
    

@login_required
def vip(request):
    try:
        subscription = request.user.subscription

        if not subscription.is_valid():
            return render(request, 'accounts/subscription_expired.html')

    except Subscription.DoesNotExist:
        return render(request, 'accounts/no_subscription.html')

    # fetch VIP codes based on user's plan
    user_plan = subscription.plan
    # subscription.plan is either 'weekly' or 'monthly'
    # but VIPCode.plan is 'safe', 'high' or 'both'
    # we need to ask the user which odds plan they subscribed to
    # for now show all codes marked as 'both'

    vip_codes = VIPCode.objects.filter(
        plan__in=['both']
        # shows codes available to all VIP subscribers
        # you can expand this based on their specific plan
    )

    paginator = Paginator(vip_codes, 10)
    page_number = request.GET.get('page')
    vip_codes = paginator.get_page(page_number)

    return render(request, 'accounts/vip.html', {
        'subscription': subscription,
        'vip_codes': vip_codes,
        'today_year': __import__('datetime').date.today().year
    })
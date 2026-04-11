from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import date
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
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def register_success(request):
    return render(request, 'accounts/register_success.html', {
        'today_year': date.today().year
    })


def user_login(request):
    # single clean login function
    # removed duplicate and incomplete @ratelimit version
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('vip')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('homepage')


@login_required
def vip(request):
    # single clean vip function
    # removed duplicate version that was missing vip_codes
    try:
        subscription = request.user.subscription

        if not subscription.is_valid():
            return render(request, 'accounts/subscription_expired.html')

    except Subscription.DoesNotExist:
        return render(request, 'accounts/no_subscription.html')

    vip_codes = VIPCode.objects.all()

    paginator = Paginator(vip_codes, 10)
    page_number = request.GET.get('page')
    vip_codes = paginator.get_page(page_number)

    return render(request, 'accounts/vip.html', {
        'subscription': subscription,
        'vip_codes': vip_codes,
        'today_year': date.today().year
    })
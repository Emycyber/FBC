from django.shortcuts import render
from .models import BookingCode, FooterLink, Partner, VIPCode, DirectWinPrediction, BettingCompany
from datetime import date, timedelta
from blog.models import BlogDetailPage
from django.core.paginator import Paginator


def homepage(request):
    today = date.today()
    todays_codes = BookingCode.objects.filter(date=today)

    paginator = Paginator(BookingCode.objects.all(), 10)
    page_number = request.GET.get('page')
    booking_codes = paginator.get_page(page_number)

    latest_posts = BlogDetailPage.objects.live().order_by('-first_published_at')[:3]

    companies = BettingCompany.objects.all()
    # fetches all betting companies to show as cards on homepage

    context = {
        'booking_codes': booking_codes,
        'todays_codes': todays_codes,
        'latest_posts': latest_posts,
        'companies': companies,
        'today_year': today.year,
        'seo_title': 'SureCodes24 - Daily Booking Codes Nigeria',
        'seo_description': 'Get free daily verified booking codes for Sportybet, Bet9ja, 1xBet and more.',
    }
    return render(request, 'bookings/homepage.html', context)


def about(request):
    context = {'today_year': date.today().year}
    return render(request, 'bookings/about.html', context)


def contact(request):
    context = {'today_year': date.today().year}
    return render(request, 'bookings/contact.html', context)


def disclaimer(request):
    context = {'today_year': date.today().year}
    return render(request, 'bookings/disclaimer.html', context)


def privacy_policy(request):
    context = {'today_year': date.today().year}
    return render(request, 'bookings/privacy_policy.html', context)


def partners(request):
    context = {
        'partners': Partner.objects.filter(is_active=True),
        'today_year': date.today().year,
    }
    return render(request, 'bookings/partners.html', context)


def pricing(request):
    context = {'today_year': date.today().year}
    return render(request, 'bookings/pricing.html', context)


def predictions(request):
    # single clean predictions view using DirectWinPrediction
    date_str = request.GET.get('date', str(date.today()))

    try:
        selected_date = date.fromisoformat(date_str)
    except ValueError:
        selected_date = date.today()
        date_str = str(selected_date)

    yesterday = str(selected_date - timedelta(days=1))
    tomorrow = str(selected_date + timedelta(days=1))

    direct_predictions = DirectWinPrediction.objects.filter(
        date=selected_date
    )

    context = {
        'direct_predictions': direct_predictions,
        'selected_date': selected_date,
        'yesterday': yesterday,
        'tomorrow': tomorrow,
        'today_year': date.today().year,
    }
    return render(request, 'bookings/predictions.html', context)


def sportybet(request):
    booking_codes = BookingCode.objects.filter(
        company__name__icontains='sportybet'
    ).order_by('-date')

    paginator = Paginator(booking_codes, 10)
    booking_codes = paginator.get_page(request.GET.get('page'))

    context = {
        'booking_codes': booking_codes,
        'company_name': 'Sportybet',
        'today_year': date.today().year,
        'seo_title': 'Sportybet Booking Codes Today - SureCodes24',
        'seo_description': 'Get free daily verified Sportybet booking codes today.',
    }
    return render(request, 'bookings/sportybet.html', context)


def bet9ja(request):
    booking_codes = BookingCode.objects.filter(
        company__name__icontains='bet9ja'
    ).order_by('-date')

    paginator = Paginator(booking_codes, 10)
    booking_codes = paginator.get_page(request.GET.get('page'))

    context = {
        'booking_codes': booking_codes,
        'company_name': 'Bet9ja',
        'today_year': date.today().year,
        'seo_title': 'Bet9ja Booking Codes Today - SureCodes24',
        'seo_description': 'Get free daily verified Bet9ja booking codes today.',
    }
    return render(request, 'bookings/bet9ja.html', context)


def bet1xbet(request):
    booking_codes = BookingCode.objects.filter(
        company__name__icontains='1xbet'
    ).order_by('-date')

    paginator = Paginator(booking_codes, 10)
    booking_codes = paginator.get_page(request.GET.get('page'))

    context = {
        'booking_codes': booking_codes,
        'company_name': '1xBet',
        'today_year': date.today().year,
        'seo_title': '1xBet Booking Codes Today - SureCodes24',
        'seo_description': 'Get free daily verified 1xBet booking codes today.',
    }
    return render(request, 'bookings/1xbet.html', context)


def betwinner(request):
    booking_codes = BookingCode.objects.filter(
        company__name__icontains='betwinner'
    ).order_by('-date')

    paginator = Paginator(booking_codes, 10)
    booking_codes = paginator.get_page(request.GET.get('page'))

    context = {
        'booking_codes': booking_codes,
        'company_name': 'Betwinner',
        'today_year': date.today().year,
        'seo_title': 'Betwinner Booking Codes Today - SureCodes24',
        'seo_description': 'Get free daily verified Betwinner booking codes today.',
    }
    return render(request, 'bookings/betwinner.html', context)


def msport(request):
    booking_codes = BookingCode.objects.filter(
        company__name__icontains='msport'
    ).order_by('-date')

    paginator = Paginator(booking_codes, 10)
    booking_codes = paginator.get_page(request.GET.get('page'))

    context = {
        'booking_codes': booking_codes,
        'company_name': 'Msport',
        'today_year': date.today().year,
        'seo_title': 'Msport Booking Codes Today - SureCodes24',
        'seo_description': 'Get free daily verified Msport booking codes today.',
    }
    return render(request, 'bookings/msport.html', context)
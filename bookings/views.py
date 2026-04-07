from django.shortcuts import render
from .models import BookingCode, BettingCompany, FooterLink, Partner, VIPCode, Prediction
from datetime import date
from blog.models import BlogDetailPage
from django.core.paginator import Paginator
from .football_api import get_fixtures
from datetime import date, timedelta



# Create your views here.

def homepage(request):
    # This view handles the homepage
    
    today = date.today()
    # Gets today's date to filter codes for today
    
    booking_codes = BookingCode.objects.all()
    # Fetches ALL booking codes from the database
    # .objects.all() is Django's way of saying "give me everything"
    
    
    
    todays_codes = BookingCode.objects.filter(date=today)
    # Fetches only today's booking codes
    # .filter() is like a WHERE clause in SQL
    # date=today means "only rows where date equals today"
    
    all_codes = BookingCode.objects.all()
    # fetches all booking codes from the database

    paginator = Paginator(all_codes, 10)
    # Paginator takes two arguments:
    # all_codes: the full list of items to paginate
    # 10: number of items to show per page

    page_number = request.GET.get('page')
    # request.GET.get('page'): reads the ?page= from the URL
    # e.g /homepage/?page=2 gives page_number = "2"
    # returns None if no page parameter in URL

    booking_codes = paginator.get_page(page_number)
    # get_page(): returns the correct page of results
    # if page_number is None it returns page 1
    # if page_number is out of range it returns the last page
    # handles all edge cases automatically
    
    latest_posts = BlogDetailPage.objects.live().order_by('-first_published_at')[:3]
    
    
    context = {
        'booking_codes': booking_codes,
        'todays_codes': todays_codes,
        'latest_posts': latest_posts,
        'today_year': date.today().year,
        'seo_title': 'FreeBetCodes - Daily Booking Codes Nigeria',
        'seo_description': 'Get free daily verified booking codes for Sportybet, Bet9ja, 1xBet and more. High odds accumulators updated every day.',
        # context is a dictionary that passes data from view to template
        # Keys become variable names in the template
    }
    
    return render(request, 'bookings/homepage.html', context)
    # render() combines the template with the context data
    # and returns it as an HTTP response to the 
    
   
def about(request):
    # About page doesn't need any database data
    # Just passes the year for the footer copyright
    context = {
        'today_year': date.today().year,
    }
    return render(request, 'bookings/about.html', context)


def contact(request):
    # Contact page doesn't need any database data
    context = {
        'today_year': date.today().year,
    }
    return render(request, 'bookings/contact.html', context)


def disclaimer(request):
    # Disclaimer page doesn't need any database data
    context = {
        'today_year': date.today().year,
    }
    return render(request, 'bookings/disclaimer.html', context)


def privacy_policy(request):
    # Privacy policy page doesn't need any database data
    context = {
        'today_year': date.today().year,
    }
    return render(request, 'bookings/privacy_policy.html', context)
    
    
    
def partners(request):
    partners = Partner.objects.filter(is_active=True)
    # filter(is_active=True): only shows active partners
    # ordered by 'order' field as defined in Meta class

    context = {
        'partners': partners,
        'today_year': date.today().year,
    }
    return render(request, 'bookings/partners.html', context)


def pricing(request):
    context = {
        'today_year': date.today().year,
    }
    return render(request, 'bookings/pricing.html', context)



def predictions(request):
    # get date from URL parameter or default to today
    date_str = request.GET.get('date', str(date.today()))
    # e.g ?date=2026-04-06

    try:
        selected_date = date.fromisoformat(date_str)
        # fromisoformat: converts string to date object
    except ValueError:
        selected_date = date.today()
        date_str = str(selected_date)

    # calculate yesterday and tomorrow for navigation buttons
    yesterday = str(selected_date - timedelta(days=1))
    tomorrow = str(selected_date + timedelta(days=1))

    # fetch fixtures from API
    fixtures = get_fixtures(date_str=date_str)
    
    # group fixtures by league
    leagues = {}
    for fixture in fixtures:
        league_name = fixture['league']['name']
        league_logo = fixture['league']['logo']

        if league_name not in leagues:
            leagues[league_name] = {
                'name': league_name,
                'logo': league_logo,
                'fixtures': []
            }
        leagues[league_name]['fixtures'].append(fixture)
        # groups all fixtures under their league name

    context = {
        'leagues': leagues,
        'selected_date': selected_date,
        'yesterday': yesterday,
        'tomorrow': tomorrow,
        'today_year': date.today().year,
    }
    return render(request, 'bookings/predictions.html', context)



def predictions(request):
    date_str = request.GET.get('date', str(date.today()))

    try:
        selected_date = date.fromisoformat(date_str)
    except ValueError:
        selected_date = date.today()
        date_str = str(selected_date)

    yesterday = str(selected_date - timedelta(days=1))
    tomorrow = str(selected_date + timedelta(days=1))

    # fetch only FREE predictions for selected date
    free_predictions = Prediction.objects.filter(
        date=selected_date,
        is_vip=False
        # is_vip=False: only show free predictions here
        # VIP predictions show on VIP page
    )

    # group by league
    leagues = {}
    for prediction in free_predictions:
        league_name = prediction.league
        if league_name not in leagues:
            leagues[league_name] = {
                'name': league_name,
                'logo': prediction.league_logo,
                'predictions': []
            }
        leagues[league_name]['predictions'].append(prediction)

    context = {
        'leagues': leagues,
        'selected_date': selected_date,
        'yesterday': yesterday,
        'tomorrow': tomorrow,
        'today_year': date.today().year,
    }
    return render(request, 'bookings/predictions.html', context)
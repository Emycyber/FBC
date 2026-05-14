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




def sportybet(request):
    today = date.today()
    booking_codes = BookingCode.objects.filter(
        company__name__icontains='sportybet'
        # icontains: case insensitive search
        # matches "Sportybet", "SportyBet", "SPORTYBET"
    ).order_by('-date')

    paginator = Paginator(booking_codes, 10)
    page_number = request.GET.get('page')
    booking_codes = paginator.get_page(page_number)

    context = {
        'booking_codes': booking_codes,
        'company_name': 'Sportybet',
        'today_year': today.year,
        'seo_title': 'Sportybet Booking Codes Today - SureCodes24',
        'seo_description': 'Get free daily verified Sportybet booking codes today. High odds accumulators updated daily by SureCodes24.',
        'faq': [
            {
                'question': 'How do I load a Sportybet booking code?',
                'answer': 'Open your Sportybet app or website, go to the booking code section, enter the code and click load. The games will appear in your betslip ready to stake.'
            },
            {
                'question': 'Are these Sportybet codes free?',
                'answer': 'Yes! All codes on this page are completely free. We also offer VIP codes with higher odds for subscribers.'
            },
            {
                'question': 'How often are Sportybet codes updated?',
                'answer': 'Our team updates Sportybet codes daily before 10am. Check back every morning for fresh codes.'
            },
            {
                'question': 'What odds range are the Sportybet codes?',
                'answer': 'Our free Sportybet codes range from 1.6 to 5.0 odds. VIP codes range from 1.8 to 2.5 for more consistent wins.'
            },
        ]
    }
    return render(request, 'bookings/sportybet.html', context)


def bet9ja(request):
    today = date.today()
    booking_codes = BookingCode.objects.filter(
        company__name__icontains='bet9ja'
    ).order_by('-date')

    paginator = Paginator(booking_codes, 10)
    page_number = request.GET.get('page')
    booking_codes = paginator.get_page(page_number)

    context = {
        'booking_codes': booking_codes,
        'company_name': 'Bet9ja',
        'today_year': today.year,
        'seo_title': 'Bet9ja Booking Codes Today - SureCodes24',
        'seo_description': 'Get free daily verified Bet9ja booking codes today. High odds accumulators updated daily by SureCodes24.',
        'faq': [
            {
                'question': 'How do I load a Bet9ja booking code?',
                'answer': 'Visit bet9ja.com or open the app, click on booking code, enter the code and click load to add the games to your betslip.'
            },
            {
                'question': 'Are these Bet9ja codes free?',
                'answer': 'Yes! All codes on this page are completely free. We also offer VIP codes with higher odds for subscribers.'
            },
            {
                'question': 'How often are Bet9ja codes updated?',
                'answer': 'Our team updates Bet9ja codes daily before 10am. Check back every morning for fresh codes.'
            },
            {
                'question': 'What odds range are the Bet9ja codes?',
                'answer': 'Our free Bet9ja codes range from 1.6 to 5.0 odds. VIP codes range from 1.8 to 2.5 for more consistent wins.'
            },
        ]
    }
    return render(request, 'bookings/bet9ja.html', context)


def bet1xbet(request):
    today = date.today()
    booking_codes = BookingCode.objects.filter(
        company__name__icontains='1xbet'
    ).order_by('-date')

    paginator = Paginator(booking_codes, 10)
    page_number = request.GET.get('page')
    booking_codes = paginator.get_page(page_number)

    context = {
        'booking_codes': booking_codes,
        'company_name': '1xBet',
        'today_year': today.year,
        'seo_title': '1xBet Booking Codes Today - SureCodes24',
        'seo_description': 'Get free daily verified 1xBet booking codes today. High odds accumulators updated daily by SureCodes24.',
        'faq': [
            {
                'question': 'How do I load a 1xBet booking code?',
                'answer': 'Login to your 1xBet account, go to the coupon section, enter the booking code and click apply to load the games.'
            },
            {
                'question': 'Are these 1xBet codes free?',
                'answer': 'Yes! All codes on this page are completely free. We also offer VIP codes with higher odds for subscribers.'
            },
            {
                'question': 'How often are 1xBet codes updated?',
                'answer': 'Our team updates 1xBet codes daily before 10am. Check back every morning for fresh codes.'
            },
            {
                'question': 'What odds range are the 1xBet codes?',
                'answer': 'Our free 1xBet codes range from 1.6 to 5.0 odds. VIP codes range from 1.8 to 2.5 for more consistent wins.'
            },
        ]
    }
    return render(request, 'bookings/1xbet.html', context)


def betwinner(request):
    today = date.today()
    booking_codes = BookingCode.objects.filter(
        company__name__icontains='betwinner'
    ).order_by('-date')

    paginator = Paginator(booking_codes, 10)
    page_number = request.GET.get('page')
    booking_codes = paginator.get_page(page_number)

    context = {
        'booking_codes': booking_codes,
        'company_name': 'Betwinner',
        'today_year': today.year,
        'seo_title': 'Betwinner Booking Codes Today - SureCodes24',
        'seo_description': 'Get free daily verified Betwinner booking codes today. High odds accumulators updated daily by SureCodes24.',
        'faq': [
            {
                'question': 'How do I load a Betwinner booking code?',
                'answer': 'Login to Betwinner, navigate to the booking code section, enter the code and click load to add all selections to your betslip.'
            },
            {
                'question': 'Are these Betwinner codes free?',
                'answer': 'Yes! All codes on this page are completely free. We also offer VIP codes with higher odds for subscribers.'
            },
            {
                'question': 'How often are Betwinner codes updated?',
                'answer': 'Our team updates Betwinner codes daily before 10am. Check back every morning for fresh codes.'
            },
            {
                'question': 'What odds range are the Betwinner codes?',
                'answer': 'Our free Betwinner codes range from 1.6 to 5.0 odds. VIP codes range from 1.8 to 2.5 for more consistent wins.'
            },
        ]
    }
    return render(request, 'bookings/betwinner.html', context)


def msport(request):
    today = date.today()
    booking_codes = BookingCode.objects.filter(
        company__name__icontains='msport'
    ).order_by('-date')

    paginator = Paginator(booking_codes, 10)
    page_number = request.GET.get('page')
    booking_codes = paginator.get_page(page_number)

    context = {
        'booking_codes': booking_codes,
        'company_name': 'Msport',
        'today_year': today.year,
        'seo_title': 'Msport Booking Codes Today - SureCodes24',
        'seo_description': 'Get free daily verified Msport booking codes today. High odds accumulators updated daily by SureCodes24.',
        'faq': [
            {
                'question': 'How do I load an Msport booking code?',
                'answer': 'Open Msport app or website, find the booking code option, enter the code and load to get all selections on your betslip.'
            },
            {
                'question': 'Are these Msport codes free?',
                'answer': 'Yes! All codes on this page are completely free. We also offer VIP codes with higher odds for subscribers.'
            },
            {
                'question': 'How often are Msport codes updated?',
                'answer': 'Our team updates Msport codes daily before 10am. Check back every morning for fresh codes.'
            },
            {
                'question': 'What odds range are the Msport codes?',
                'answer': 'Our free Msport codes range from 1.6 to 5.0 odds. VIP codes range from 1.8 to 2.5 for more consistent wins.'
            },
        ]
    }
    return render(request, 'bookings/msport.html', context)
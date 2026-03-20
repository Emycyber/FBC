from django.shortcuts import render
from .models import BookingCode, BettingCompany
from datetime import date
from blog.models import BlogDetailPage
from django.core.paginator import Paginator



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
    
    
    
    
    

# Paginator: Django's built in pagination class



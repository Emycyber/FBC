from django.http import HttpResponse
from django.urls import path
from django.views.generic import TemplateView

from . import views

# Dynamic text delivery bypasses the broken Django template engine lookup
def clean_robots_text_fallback(request):
    rules = (
        "User-agent: *\n"
        "Allow: /\n\n"
        "Sitemap: https://surecodes24.com/sitemap.xml"  # FIXED: Pointing to exact file
    )
    return HttpResponse(rules, content_type="text/plain")


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("disclaimer/", views.disclaimer, name="disclaimer"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("partners/", views.partners, name="partners"),
    path("pricing/", views.pricing, name="pricing"),
    path("direct-win-prediction/", views.predictions, name="predictions"),
    
    # Bookmaker filters
    path("sportybet-booking-codes/", views.sportybet, name="sportybet"),
    path("bet9ja-booking-codes/", views.bet9ja, name="bet9ja"),
    path("1xbet-booking-codes/", views.bet1xbet, name="1xbet"),
    path("betwinner-booking-codes/", views.betwinner, name="betwinner"),
    path("msport-booking-codes/", views.msport, name="msport"),
    
    # The native robots path configuration
    path("robots.txt", clean_robots_text_fallback, name="robots"),
]

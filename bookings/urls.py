from django.urls import path
from . import views
from django.views.generic import TemplateView

# Importing views from the current bookings app
# The dot (.) means "from this same folder/app"

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('partners/', views.partners, name='partners'),
    path('pricing/', views.pricing, name='pricing'),
    path('direct-win-prediction/', views.predictions, name='predictions'),
    # ← add this
    
    
    path('sportybet-booking-codes/', views.sportybet, name='sportybet'),
    path('bet9ja-booking-codes/', views.bet9ja, name='bet9ja'),
    path('1xbet-booking-codes/', views.bet1xbet, name='1xbet'),
    path('betwinner-booking-codes/', views.betwinner, name='betwinner'),
    path('msport-booking-codes/', views.msport, name='msport'),
    
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain',
    ), name='robots'),
]

from django.urls import path
from . import views
# Importing views from the current bookings app
# The dot (.) means "from this same folder/app"

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('partners/', views.partners, name='partners'),
    # ← add this
]
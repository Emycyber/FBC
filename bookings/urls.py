from django.urls import path
from . import views
# Importing views from the current bookings app
# The dot (.) means "from this same folder/app"

urlpatterns = [
    path('', views.homepage, name='homepage'),
    # '' means the root URL e.g yourdomain.com/
    # views.homepage is the function to call when this URL is visited
    # name='homepage' lets you reference this URL as {% url 'homepage' %} in templates
]
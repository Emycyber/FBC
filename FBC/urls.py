"""
URL configuration for FBC project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from bookings import views as bookings_views
from django.conf import settings
from django.conf.urls.static import static
# static() serves uploaded media files during development

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('', include('bookings.urls')), 
    path('', include(wagtail_urls)),
    path('contact', bookings_views.contact, name='contact'),
    path('about', bookings_views.about, name='about'),
    path('disclaimer', bookings_views.disclaimer, name='disclaimer'),
    path('privacy_policy', bookings_views.privacy_policy, name='privacy_policy'),
       
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


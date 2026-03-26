from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path('django-admin/', admin.site.urls),
    # Django admin panel

    path('admin/', include(wagtailadmin_urls)),
    # Wagtail admin panel

    path('documents/', include(wagtaildocs_urls)),
    # Wagtail document downloads

    path('', include('bookings.urls')),
    # All bookings app URLs including homepage,
    # about, contact, disclaimer, privacy policy, partners

    path('', include(wagtail_urls)),
    # Wagtail handles blog and CMS pages
    # must be LAST so it acts as a fallback

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
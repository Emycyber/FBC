from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from bookings.sitemaps import StaticViewSitemap, WagtailSitemap
from django.contrib.sitemaps.views import sitemap


sitemaps = {
    'static': StaticViewSitemap,
    'wagtail': WagtailSitemap,
    # combines both sitemaps into one sitemap.xml file
}


urlpatterns = [
    path('django-admin/', admin.site.urls),
    # Django admin panel

    path('admin/', include(wagtailadmin_urls)),
    # Wagtail admin panel

    path('documents/', include(wagtaildocs_urls)),
    # Wagtail document downloads
    
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

    path('', include('bookings.urls')),
    # All bookings app URLs including homepage,
    # about, contact, disclaimer, privacy policy, partners
    
    path('accounts/', include('accounts.urls')),


    path('', include(wagtail_urls)),
    # Wagtail handles blog and CMS pages
    # must be LAST so it acts as a fallback

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


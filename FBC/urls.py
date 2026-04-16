from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from bookings.sitemaps import StaticViewSitemap, WagtailSitemap
from bookings.api_admin_views import api_football_view

sitemaps = {
    'static': StaticViewSitemap,
    'wagtail': WagtailSitemap,
}

urlpatterns = [
    path('django-admin/api-football/', api_football_view, name='api_football'),
    # ✅ must come before django-admin/

    path('django-admin/', admin.site.urls),
    # ✅ correct django admin URL

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('', include('bookings.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include(wagtail_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
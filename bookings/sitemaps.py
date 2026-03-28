from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from wagtail.models import Page


class StaticViewSitemap(Sitemap):
    # Sitemap for your static Django pages
    priority = 0.8
    changefreq = 'weekly'
    # changefreq: tells Google how often pages change
    # weekly: Google checks these pages once a week

    def items(self):
        return [
            'homepage',
            'about',
            'contact',
            'disclaimer',
            'privacy_policy',
            'partners',
        ]
        # list of URL names from your bookings/urls.py

    def location(self, item):
        return reverse(item)
        # reverse(): converts URL name to actual URL
        # e.g 'about' becomes '/about/'


class WagtailSitemap(Sitemap):
    # Sitemap for your Wagtail blog pages
    priority = 0.9
    changefreq = 'daily'
    # daily: blog posts change more frequently

    def items(self):
        return Page.objects.live().public()
        # .live(): only published pages
        # .public(): only publicly accessible pages

    def location(self, page):
        return page.url_path
        # url_path: Wagtail's built in URL for each page
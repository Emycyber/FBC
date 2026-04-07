from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from wagtail.models import Page


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'

    def items(self):
        return [
            'homepage',
            'about',
            'contact',
            'disclaimer',
            'privacy_policy',
            'partners',
            'pricing',
            'predictions',
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        # different priority for each page type
        # tells Google which pages are most important
        priorities = {
            'homepage': 1.0,
            # homepage is most important page
            'predictions': 0.9,
            # predictions changes daily so high priority
            'pricing': 0.9,
            # pricing page important for conversions
            'about': 0.6,
            'contact': 0.6,
            'partners': 0.5,
            'disclaimer': 0.3,
            'privacy_policy': 0.3,
            # legal pages least important for SEO
        }
        return priorities.get(item, 0.5)
        # default 0.5 if page not in dictionary

    def changefreq(self, item):
        # different update frequency for each page
        frequencies = {
            'homepage': 'daily',
            # homepage updates daily with new codes
            'predictions': 'daily',
            # predictions change every day
            'pricing': 'monthly',
            # pricing rarely changes
            'about': 'monthly',
            'contact': 'monthly',
            'partners': 'weekly',
            'disclaimer': 'yearly',
            'privacy_policy': 'yearly',
        }
        return frequencies.get(item, 'weekly')


class WagtailSitemap(Sitemap):
    # Sitemap for Wagtail blog pages
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return Page.objects.live().public()
        # .live(): only published pages
        # .public(): only publicly accessible pages

    def location(self, page):
        return page.url_path
        # url_path: Wagtail's built in URL for each page
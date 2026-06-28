from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from wagtail.models import Page


class StaticViewSitemap(Sitemap):

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
            'sportybet',
            'bet9ja',
            '1xbet',
            'betwinner',
            'msport',
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        priorities = {
            'homepage': 1.0,
            'predictions': 0.9,
            'pricing': 0.9,
            'sportybet': 0.9,
            'bet9ja': 0.9,
            '1xbet': 0.9,
            'betwinner': 0.9,
            'msport': 0.9,
            'about': 0.6,
            'contact': 0.6,
            'partners': 0.5,
            'disclaimer': 0.3,
            'privacy_policy': 0.3,
        }
        return priorities.get(item, 0.5)

    def changefreq(self, item):
        frequencies = {
            'homepage': 'daily',
            'predictions': 'daily',
            'sportybet': 'daily',
            'bet9ja': 'daily',
            '1xbet': 'daily',
            'betwinner': 'daily',
            'msport': 'daily',
            'pricing': 'monthly',
            'about': 'monthly',
            'contact': 'monthly',
            'partners': 'weekly',
            'disclaimer': 'yearly',
            'privacy_policy': 'yearly',
        }
        return frequencies.get(item, 'weekly')


class WagtailSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return Page.objects.live().public()

    def location(self, page):
        return page.url_path